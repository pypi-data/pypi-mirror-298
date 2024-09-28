import asyncio
import logging
from collections import deque
from time import sleep

from decentnet.consensus.dev_constants import RUN_IN_DEBUG
from decentnet.modules.logger.log import setup_logger

logger = logging.getLogger(__name__)

setup_logger(RUN_IN_DEBUG, logger)


class ReqQueue:
    _requeue: deque = None

    @classmethod
    def append(cls, func):
        if cls._requeue is not None:
            cls._requeue.append(func)

    @classmethod
    def init_queue(cls):
        cls._requeue = deque()

    @classmethod
    def do_requests(cls):
        logger.debug("Starting request queue")
        cls.init_queue()
        while True:
            try:
                asyncio.run(cls._requeue.pop())
            except IndexError:
                sleep(1.5)
