import queue
import socket

from . import StructPlus
from . import ThreadingPlus


# module end at 8/1/2024
# module start at 8/21/2024  # 完成一个远程代理服务类
# module end at 8/23/2024 # 代理服务类没做完，做完了一个简单的服务器类
# 基于此的BoardcastRoom仍处于开发状态


class _BaseSimpleSocket:
    def __init__(self, s: socket.socket | object | None = None):
        self.read_loop_event = None
        self.write_loop_event = None
        self.read_thread = None
        self.write_thread = None
        if s is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        elif isinstance(s, self.__class__):
            self.sock = s.sock

        self.lasterror = None
        self._buffer = queue.Queue(256)
        self._write_buffer = queue.Queue(256)

    def set(self, sock, start_server=True):
        self.sock.close()
        self.sock = sock  # type: socket.socket
        if start_server:
            self.start_server()

    def close(self):
        self.stop_server()
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
        except OSError as e:
            self.lasterror = e
        self.sock.close()

    def getlasterror(self):
        e = self.lasterror
        self.lasterror = None
        return e

    def settimeout(self, timeout):
        self.sock.settimeout(timeout)

    def connect(self, host, port, timeout=None):
        try:
            self.sock.settimeout(timeout)
            self.sock.connect((host, port))
            self.getlasterror()
            self.start_server()
            return True
        except socket.error as e:
            self.lasterror = e
            return False

    def bindport(self, port):  # 绑定端口
        try:
            self.sock.bind(('', port))
            self.getlasterror()
            return True
        except socket.error as e:
            self.lasterror = e
            return False

    def bind(self, host, port):  # 绑定端口
        try:
            self.sock.bind((host, port))
            self.getlasterror()
            return True
        except socket.error as e:
            self.lasterror = e
            return False

    def listen(self, backlog=1):
        try:
            self.sock.listen(backlog)
            self.getlasterror()
            return True
        except socket.error as e:
            self.lasterror = e
            return False

    def accept(self):
        conn, addr = self.sock.accept()
        conn_simple = self.__class__()
        conn_simple.set(conn)
        conn_simple.start_server()
        return conn_simple, addr

    def _write(self, data):
        packing_data_bytes = StructPlus.simple_jsonpickle_pack(data)

        try:
            self.sock.sendall(packing_data_bytes)
            self.getlasterror()
            return True
        except socket.error as e:
            self.lasterror = e
            return False

    def _read_loop(self, StopEvent):
        while True:
            if StopEvent.is_set():
                return

            data = self._read()
            if data is not None:
                for item in data:
                    self._buffer.put(item)

    def _read(self):
        every_data = b""
        try:
            while True:
                every_data += self.sock.recv(65535)
                if len(every_data) < 65535:
                    break

        except socket.herror as e:
            self.lasterror = e
            return None

        if every_data == b'':
            return None

        unpacking_datas = StructPlus.simple_jsonpickle_unpacks(every_data)
        return unpacking_datas

    def read(self, timeout=None):
        try:
            data = self._buffer.get(timeout=timeout)
            self._buffer.task_done()
        except queue.Empty:
            return None
        return data

    def write(self, data):
        self._write_buffer.put(data)

    def _write_loop(self, StopEvent):
        while StopEvent.is_set():
            try:
                data = self._write_buffer.get(timeout=0.5)
                self._write(data)
                self._write_buffer.task_done()
            except queue.Empty:
                continue

    def empty(self):
        return self._buffer.empty()

    def start_server(self):
        if self.read_thread is not None and self.write_thread is not None:
            self.read_loop_event = ThreadingPlus.threading.Event()
            self.write_loop_event = ThreadingPlus.threading.Event()
            self.read_thread = ThreadingPlus.start_new_thread(self._read_loop, self.read_loop_event)
            self.write_thread = ThreadingPlus.start_new_thread(self._write_loop, self.write_loop_event)

    def stop_server(self):
        if self.read_thread is not None:
            self.read_loop_event.set()
        if self.write_thread is not None:
            self.write_loop_event.set()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


Sockets = socket.socket | _BaseSimpleSocket


class Socket:
    def __init__(self, s: Sockets | object | None = None):
        if isinstance(s, _BaseSimpleSocket):
            self._socket = s
        else:
            self._socket = _BaseSimpleSocket(s)

    @property
    def sock(self):
        return self._socket.sock

    @property
    def base_socket(self):
        return self._socket

    def set(self, sock, start_server=True):
        self._socket.set(sock, start_server)

    def close(self):
        self._socket.close()

    def getlasterror(self):
        return self._socket.getlasterror()

    def settimeout(self, timeout):
        self._socket.settimeout(timeout)

    def connect(self, host, port, timeout=None):
        return self._socket.connect(host, port, timeout)

    def bindport(self, port):
        return self._socket.bindport(port)

    def bind(self, host, port):
        return self._socket.bind(host, port)

    def listen(self, backlog=1):
        return self._socket.listen(backlog)

    def accept(self):
        conn, addr = self._socket.accept()
        return Socket(conn), addr

    def read(self, timeout=None):
        return self._socket.read(timeout)

    def write(self, data):
        self._socket.write(data)

    def empty(self):
        return self._socket.empty()

    def start_server(self):
        self._socket.start_server()

    def stop_server(self):
        self._socket.stop_server()

    def self_accept(self):
        self._socket.close()
        self._socket = self._socket.accept()[0]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def is_tcp(s: Socket | socket.socket):
    if isinstance(s, Socket):
        return is_tcp(s.sock)
    else:
        return s.type == socket.SOCK_STREAM


def is_udp(s: Socket | socket.socket):
    if isinstance(s, Socket):
        return is_udp(s.sock)
    else:
        return s.type == socket.SOCK_DGRAM
