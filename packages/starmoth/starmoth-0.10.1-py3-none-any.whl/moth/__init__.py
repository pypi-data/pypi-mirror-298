import logging
import zmq
import time
import queue
import threading
from typing import Optional, List

from moth.log import configure_moth_logger
from moth.message import (
    HandshakeMsg,
    HandshakeResponseMsg,
    HeartbeatMsg,
    ImagePromptMsg,
    parse_message,
    HandshakeTaskTypes,
)
from moth.message.exceptions import MothMessageError

configure_moth_logger()
logger = logging.getLogger(__name__)
class Moth:
    _PROMPT_FUNCTIONS = []
    _MATH_FUNCTIONS = []
    HEARTBEAT_TIMEOUT = 5
    HEARTBEAT_INTERVAL = 1

    def __init__(
        self,
        name: str,
        token: str = "",
        task_type: HandshakeTaskTypes = HandshakeTaskTypes.CLASSIFICATION,
        output_classes: Optional[List[str]] = None,
    ):
        self.name = name
        self._token = token
        self.stop = False
        self.task_type = task_type
        self.output_classes = output_classes

    def run(self, url="tcp://localhost:7171"):
        self.stop = False
        context = zmq.Context()
        socket = context.socket(zmq.DEALER)
        socket.setsockopt_string(zmq.IDENTITY, self.name)

        try:
            socket.connect(url)
            # This is a handshake call to prove our identity
            handshake = HandshakeMsg(
                self.name, self._token, "v0.0.0", self.task_type, self.output_classes
            )
            socket.send(handshake.serialize_envelope())
            self._req_loop(socket)
        except KeyboardInterrupt:
            logger.info("KeyboardInterrupt")
            print("\nExit...")
            self.stop = True

    def prompt(self, func):
        self._PROMPT_FUNCTIONS.append(func)
        return func

    def math(self, func):
        self._MATH_FUNCTIONS.append(func)
        return func

    def _req_loop(self, socket):
        pool = zmq.Poller()
        pool.register(socket, zmq.POLLIN)

        last_heartbeat = None
        last_heartbeat_sent = time.time()
        result_queue = queue.Queue()
        prompt_queue = queue.Queue()

        # Workers to handle prompts
        def prompt_loop():
            try:
                while not self.stop:
                    func = self._PROMPT_FUNCTIONS[0]
                    message = prompt_queue.get()
                    result_queue.put(func(message))
                    logger.debug(f"result_queue: {result_queue.qsize()}")
            except Exception as err:
                logger.error(f"Failed to handle prompt: {err}")
                logger.exception(err)
                print("Failed to handle prompt: ", err)
                self.stop = True

        threading.Thread(target=prompt_loop, daemon=True).start()

        while not self.stop:
            try:
                events = dict(pool.poll(1000))

                while not result_queue.empty():
                    result = result_queue.get()
                    socket.send(result.serialize_envelope())

                if events:
                    # Check if the prompt queue is empty
                    msg_bytes = socket.recv()
                    message = parse_message(msg_bytes)

                    if isinstance(message, ImagePromptMsg):
                        prompt_queue.put(message)
                        logger.debug(f"prompt_queue: {prompt_queue.qsize()}")
                        last_heartbeat = time.time()

                    if isinstance(message, HeartbeatMsg):
                        logger.debug(f"Got heartbeat from server")
                        last_heartbeat = time.time()

                    if isinstance(message, HandshakeResponseMsg):
                        logger.info("Connected to server")
                        last_heartbeat = time.time()

                if (
                    last_heartbeat is not None
                    and time.time() - last_heartbeat > self.HEARTBEAT_TIMEOUT
                ):
                    logger.debug(f"Time since heartbeat: {time.time() - last_heartbeat}")
                    logger.info("Lost connection to server")
                    self.stop = True

                if time.time() - last_heartbeat_sent > self.HEARTBEAT_INTERVAL:
                    try:
                        logger.debug(f"Send heartbeat")
                        socket.send(HeartbeatMsg().serialize_envelope())
                        last_heartbeat_sent = time.time()
                    except Exception as err:
                        logger.error(f"Failed to send heartbeat: {err}")
                        logger.exception(err)
            except MothMessageError as err:
                logger.error(f"Failed to parse this message: {err}")

        socket.close()


def main():
    print(
        """
    ███╗░░░███╗░█████╗░████████╗██╗░░██╗
    ████╗░████║██╔══██╗╚══██╔══╝██║░░██║
    ██╔████╔██║██║░░██║░░░██║░░░███████║
    ██║╚██╔╝██║██║░░██║░░░██║░░░██╔══██║
    ██║░╚═╝░██║╚█████╔╝░░░██║░░░██║░░██║
    ╚═╝░░░░░╚═╝░╚════╝░░░░╚═╝░░░╚═╝░░╚═╝
    """
    )
