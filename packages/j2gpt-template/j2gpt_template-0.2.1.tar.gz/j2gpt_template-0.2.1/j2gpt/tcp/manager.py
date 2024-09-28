from socket import socket as Socket, AddressFamily, SocketKind
from contextlib import contextmanager
from typing import Generator, Callable
from j2gpt.tcp.client import Client

@contextmanager
def client(on_receive: Callable[[str], None],
           timeout: float | None = None,
           host: str = 'localhost',
           port: int = 50027) -> Generator[Client, None, None]:
    try:
        socket: Socket = Socket(family=AddressFamily.AF_INET,
                                type=SocketKind.SOCK_STREAM)
        socket.connect((host, port))
        client: Client = Client(socket=socket, on_receive=on_receive)
        yield client
    finally:
        client.join(timeout=timeout)
        client.close()