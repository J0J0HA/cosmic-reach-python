import io
import socket
import traceback
from collections import defaultdict
from typing import Any, Callable

from ..protocol import GamePacket, get_packet_registry


class SocketReadBuffer:
    def __init__(self, sock: socket.socket):
        self.sock = sock

    def read(self, length):
        return self.sock.recv(length)

    def write(self, buf: io.BytesIO):
        return self.sock.send(buf)


class BaseClient:
    "A barebones client, just being able to send and receive packets, nothing more."

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.buffer = SocketReadBuffer(self.sock)
        self.event_handlers = defaultdict(list)
        self.packet_registry = get_packet_registry()

    def send_packet(self, packet: GamePacket):
        "Send a packet to the connected server"
        self.buffer.write(self.packet_registry.serialize_packet(packet))

    def receive_packet(self) -> GamePacket:
        """Receive on packet from the connected server

        If no packet is waiting in the buffer, this function will wait until one package is received.
        """
        return self.packet_registry.deserialize_packet(self.buffer)

    def connect(self, host: str = "localhost", port: int = 47137):
        """Connect the client to a remote server

        :param host: The host of the remote server
        :param port: The port of the remote server
        """
        self.sock.connect((host, port))
        self._event_call("connecting")

    # def disconnect(self):
    #     self.sock.close()

    def add_event_handler(
        self, event: str, handler: Callable, condition: Any | None = None
    ):
        """Add an event handler

        Some events might have so-called :code:``conditions``,
        for example to differenciate between different packets.

        If you supply :py:const:``None`` for the :code:``conditions`` parameter,
        the handler will be executed in every occurenece of given event.

        If you supply a value for the :code:``conditions`` parameter,
        the handler will only be executed when the cause of the event is equal to the given value.
        Please read the documentation of a specific event for possible values.

        :param event: The event to listen for
        :param handler: The handler to call when the event is triggered
        :param condition: The condition that must be met for the handler to be called
        """
        self.event_handlers[event].append((handler, condition))

    def on(
        self, event: str, condition: Any | None = None
    ) -> Callable[[Callable[..., None]], Callable]:
        """Decorator to add an event handler

        Some events might have so-called :code:``conditions``,
        for example to differenciate between different packets.

        If you supply :py:const:``None`` for the :code:``conditions`` parameter,
        the handler will be executed in every occurenece of given event.

        If you supply a value for the :code:``conditions`` parameter,
        the handler will only be executed when the cause of the event is equal to the given value.
        Please read the documentation of a specific event for possible values.

        :param event: The event to listen for
        :param condition: The condition that must be met for the handler to be called
        """
        return lambda handler: self.add_event_handler(event, handler, condition)

    def _event_call(
        self,
        event: str,
        condition: Any | None = None,
        pass_args: tuple[Any] | None = None,
        pass_kwargs: dict[str, Any] | None = None,
    ):
        pass_args = pass_args or tuple()
        pass_kwargs = pass_kwargs or dict()
        for handler, handler_condition in self.event_handlers[event]:
            if (
                condition is None
                or handler_condition is None
                or condition == handler_condition
            ):
                handler(*pass_args, **pass_kwargs)

    def receive_packets(self):
        "Infinitely receive and handle packets"
        while self.sock:
            try:
                packet = self.receive_packet()
            except Exception as e:
                print("----- ERROR -----")
                traceback.print_exception(e)
                print("-----------------")
            else:
                self._event_call("packet", type(packet), (packet,))
