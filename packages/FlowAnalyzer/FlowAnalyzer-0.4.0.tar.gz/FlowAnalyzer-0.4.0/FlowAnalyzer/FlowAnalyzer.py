import contextlib
import gzip
import hashlib
import json
import os
import subprocess
from dataclasses import dataclass
from typing import Dict, Iterable, NamedTuple, Optional, Tuple
from urllib import parse

from .logging_config import logger
from .Path import get_default_tshark_path


@dataclass
class Request:
    frame_num: int
    header: bytes
    file_data: bytes
    full_uri: str
    time_epoch: float


@dataclass
class Response:
    frame_num: int
    header: bytes
    file_data: bytes
    time_epoch: float
    _request_in: Optional[int]


class HttpPair(NamedTuple):
    request: Optional[Request]
    response: Optional[Response]


class FlowAnalyzer:
    """FlowAnalyzer是一个流量分析器，用于解析和处理tshark导出的JSON数据文件"""

    def __init__(self, json_path: str):
        """初始化FlowAnalyzer对象

        Parameters
        ----------
        json_path : str
            tshark导出的JSON文件路径
        """
        self.json_path = json_path
        self.check_json_file()

    def check_json_file(self):
        # sourcery skip: replace-interpolation-with-fstring
        """检查JSON文件是否存在并非空

        Raises
        ------
        FileNotFoundError
            当JSON文件不存在时抛出异常
        ValueError
            当JSON文件内容为空时抛出异常
        """
        if not os.path.exists(self.json_path):
            raise FileNotFoundError("您的tshark导出的JSON文件没有找到！JSON路径：%s" % self.json_path)

        if os.path.getsize(self.json_path) == 0:
            raise ValueError("您的tshark导出的JSON文件内容为空！JSON路径：%s" % self.json_path)

    def parse_packet(self, packet: dict) -> Tuple[int, int, float, str, str]:
        """解析Json中的关键信息字段

        Parameters
        ----------
        packet : dict
            传入Json字典

        Returns
        -------
        Tuple[int, int, float, str, str]
            frame_num, request_in, time_epoch, full_uri, full_request
        """
        frame_num = int(packet["frame.number"][0])
        request_in = int(packet["http.request_in"][0]) if packet.get("http.request_in") else frame_num
        full_uri = parse.unquote(packet["http.request.full_uri"][0]) if packet.get("http.request.full_uri") else ""
        time_epoch = float(packet["frame.time_epoch"][0])

        if packet.get("tcp.reassembled.data"):
            full_request = packet["tcp.reassembled.data"][0]
        elif packet.get("tcp.payload"):
            full_request = packet["tcp.payload"][0]
        else:
            # exported_pdu.exported_pdu
            full_request = packet["exported_pdu.exported_pdu"][0]
        return frame_num, request_in, time_epoch, full_uri, full_request

    def parse_http_json(self) -> Tuple[Dict[int, Request], Dict[int, Response]]:
        """解析JSON数据文件中的HTTP请求和响应信息

        Returns
        -------
        tuple
            包含请求字典和响应列表的元组
        """
        with open(self.json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        requests, responses = {}, {}
        for packet in data:
            packet = packet["_source"]["layers"]
            frame_num, request_in, time_epoch, full_uri, full_request = self.parse_packet(packet)
            header, file_data = self.extract_http_file_data(full_request)

            # 请求包使用 full_uri 来记录请求 url  返回包使用 request_in 来记录请求包的序号
            if packet.get("http.response.code"):
                responses[frame_num] = Response(
                    frame_num=frame_num,
                    _request_in=request_in,
                    header=header,
                    file_data=file_data,
                    time_epoch=time_epoch,
                )
            else:
                requests[frame_num] = Request(
                    frame_num=frame_num, header=header, file_data=file_data, time_epoch=time_epoch, full_uri=full_uri
                )
        return requests, responses

    def generate_http_dict_pairs(self) -> Iterable[HttpPair]:  # sourcery skip: use-named-expression
        """生成HTTP请求和响应信息的字典对
        Yields
        ------
        Iterable[HttpPair]
            包含请求和响应信息的字典迭代器
        """
        requests, responses = self.parse_http_json()
        response_map = {r._request_in: r for r in responses.values()}
        yielded_resps = []
        for req_id, req in requests.items():
            resp = response_map.get(req_id)
            if resp:
                yielded_resps.append(resp)
                resp._request_in = None
                yield HttpPair(request=req, response=resp)
            else:
                yield HttpPair(request=req, response=None)

        for resp in response_map.values():
            if resp not in yielded_resps:
                resp._request_in = None
                yield HttpPair(request=None, response=resp)

    @staticmethod
    def get_hash(file_path: str, display_filter: str) -> str:
        with open(file_path, "rb") as f:
            return hashlib.md5(f.read() + display_filter.encode()).hexdigest()

    @staticmethod
    def extract_json_file(file_name: str, display_filter: str, tshark_path: str, tshark_work_dir: str, json_work_path: str) -> None:
        command = [
            tshark_path,
            "-r",
            file_name,
            "-Y",
            f"({display_filter})",
            "-T",
            "json",
            "-e",
            "http.response.code",
            "-e",
            "http.request_in",
            "-e",
            "tcp.reassembled.data",
            "-e",
            "frame.number",
            "-e",
            "tcp.payload",
            "-e",
            "frame.time_epoch",
            "-e",
            "exported_pdu.exported_pdu",
            "-e",
            "http.request.full_uri",
        ]
        logger.debug(f"导出Json命令: {command}")

        with open(json_work_path, "wb") as output_file:
            process = subprocess.Popen(command, stdout=output_file, stderr=subprocess.PIPE, cwd=tshark_work_dir)
            _, stderr = process.communicate()
        logger.debug(f"导出Json文件路径: {json_work_path}")

        if stderr and b"WARNING" not in stderr:
            try:
                print(f"[Warning/Error]: {stderr.decode('utf-8')}")
            except Exception:
                print(f"[Warning/Error]: {stderr.decode('gbk')}")

    @staticmethod
    def add_md5sum(json_work_path: str, md5_sum: str) -> None:
        with open(json_work_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        data[0]["MD5Sum"] = md5_sum

        with open(json_work_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    @staticmethod
    def get_json_data(file_path: str, display_filter: str, tshark_path: Optional[str] = None) -> str:
        # sourcery skip: replace-interpolation-with-fstring
        """获取JSON数据并保存至文件，保存目录是当前工作目录，也就是您运行脚本所在目录

        Parameters
        ----------
        file_path : str
            待处理的数据文件路径
        display_filter : str
            WireShark的显示过滤器

        Returns
        -------
        str
            保存JSON数据的文件路径
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError("您的填写的流量包没有找到！流量包路径：%s" % file_path)

        md5_sum = FlowAnalyzer.get_hash(file_path, display_filter)
        logger.debug(f"md5校验值: {md5_sum}")

        work_dir = os.getcwd()
        tshark_command_work_dir = os.path.dirname(os.path.abspath(file_path))
        json_work_path = os.path.join(work_dir, "output.json")
        file_name = os.path.basename(file_path)

        if os.path.exists(json_work_path):
            try:
                with open(json_work_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if data[0].get("MD5Sum") == md5_sum:
                        logger.debug("匹配md5校验无误，自动返回Json文件路径!")
                        return json_work_path
            except Exception:
                logger.debug("默认的Json文件无法被正常解析, 正在重新生成Json文件中")

        tshark_path = FlowAnalyzer.get_tshark_path(tshark_path)
        FlowAnalyzer.extract_json_file(file_name, display_filter, tshark_path, tshark_command_work_dir, json_work_path)
        FlowAnalyzer.add_md5sum(json_work_path, md5_sum)
        return json_work_path

    @staticmethod
    def get_tshark_path(tshark_path: Optional[str]) -> str:
        default_tshark_path = get_default_tshark_path()
        if not os.path.exists(default_tshark_path):
            logger.debug("没有检测到tshark存在, 请查看并检查tshark_path")
        else:
            logger.debug("检测到默认tshark存在!")

        if tshark_path is None:
            logger.debug("您没有传入tshark_path, 请传入tshark_path")
        elif not os.path.exists(tshark_path):
            logger.debug("传入的tshark_path不存在, 请查看并检查tshark_path")

        use_tshark_path = None
        if os.path.exists(default_tshark_path):
            use_tshark_path = default_tshark_path

        if tshark_path is not None and os.path.exists(tshark_path):
            use_tshark_path = tshark_path

        if use_tshark_path is None:
            logger.critical("您没有配置 tshark_path 并且没有在参数中传入 tshark_path")
            exit(-1)
        return use_tshark_path

    def split_http_headers(self, file_data: bytes) -> Tuple[bytes, bytes]:
        headerEnd = file_data.find(b"\r\n\r\n")
        if headerEnd != -1:
            headerEnd += 4
            return file_data[:headerEnd], file_data[headerEnd:]
        elif file_data.find(b"\n\n") != -1:
            headerEnd = file_data.index(b"\n\n") + 2
            return file_data[:headerEnd], file_data[headerEnd:]
        else:
            print("[Warning] 没有找到headers和response的划分位置!")
            return b"", file_data

    def dechunck_http_response(self, file_data: bytes) -> bytes:
        """解码分块TCP数据

        Parameters
        ----------
        file_data : bytes
            已经切割掉headers的TCP数据

        Returns
        -------
        bytes
            解码分块后的TCP数据
        """
        chunks = []
        chunkSizeEnd = file_data.find(b"\n") + 1
        lineEndings = b"\r\n" if bytes([file_data[chunkSizeEnd - 2]]) == b"\r" else b"\n"
        lineEndingsLength = len(lineEndings)
        while True:
            chunkSize = int(file_data[:chunkSizeEnd], 16)
            if not chunkSize:
                break

            chunks.append(file_data[chunkSizeEnd : chunkSize + chunkSizeEnd])
            file_data = file_data[chunkSizeEnd + chunkSize + lineEndingsLength :]
            chunkSizeEnd = file_data.find(lineEndings) + lineEndingsLength
        return b"".join(chunks)

    def extract_http_file_data(self, full_request: str) -> Tuple[bytes, bytes]:
        """提取HTTP请求或响应中的文件数据

        Parameters
        ----------
        full_request : bytes
            HTTP请求或响应的原始字节流

        Returns
        -------
        tuple
            包含header和file_data的元组
        """
        header, file_data = self.split_http_headers(bytes.fromhex(full_request))

        with contextlib.suppress(Exception):
            file_data = self.dechunck_http_response(file_data)

        with contextlib.suppress(Exception):
            if file_data.startswith(b"\x1f\x8b"):
                file_data = gzip.decompress(file_data)
        return header, file_data
