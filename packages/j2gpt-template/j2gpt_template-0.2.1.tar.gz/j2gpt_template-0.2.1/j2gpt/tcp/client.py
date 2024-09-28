from socket import socket as Socket
from threading import Thread
from dataclasses import dataclass, field
from typing import Callable, NoReturn

@dataclass(slots=True)
class Client:
    socket: Socket
    on_receive: Callable[[str], NoReturn]
    receive_thread: Thread | None = field(default=None, init=False)

    def __post_init__(self) -> None:
        def receive() -> None:
            while True:
                try:
                    size: int = int(self.socket.recv(16).decode(encoding='UTF-8').strip())
                    message: str = self.socket.recv(size).decode(encoding='UTF-8')
                    self.on_receive(message)
                except Exception as e:
                    print(e)
        self.receive_thread = Thread(target=receive, daemon=True)
        self.receive_thread.start()

    def send(self, message: str) -> None:
        data: bytes = message.encode(encoding='UTF-8')
        size: bytes = f'{len(data):16}'.encode(encoding='UTF-8')
        self.socket.send(size)
        self.socket.send(data)

    def join(self, timeout: float | None = None) -> None:
        self.receive_thread.join(timeout=timeout)

    def close(self) -> None:
        self.socket.close()