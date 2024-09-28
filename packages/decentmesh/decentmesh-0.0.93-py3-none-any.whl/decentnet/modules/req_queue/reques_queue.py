import asyncio
import logging
from collections import deque
from time import sleep

from decentnet.consensus.dev_constants import RUN_IN_DEBUG
from decentnet.consensus.metrics_constants import MAX_REQUEST_QUEUE_LEN
from decentnet.modules.logger.log import setup_logger

logger = logging.getLogger(__name__)

setup_logger(RUN_IN_DEBUG, logger)


class ReqQueue:
    _requeue: deque = None
    item_count: int = 0

    @classmethod
    def append(cls, func):
        if cls._requeue is not None:
            while cls.item_count >= MAX_REQUEST_QUEUE_LEN:
                logger.debug("Waiting for request queue to empty out")
                sleep(1)
            cls._requeue.append(func)
            cls.item_count += 1

    @classmethod
    def init_queue(cls):
        cls._requeue = deque(maxlen=MAX_REQUEST_QUEUE_LEN)

    @classmethod
    def do_requests(cls):
        logger.debug("Starting request queue")
        cls.init_queue()
        while True:
            try:
                asyncio.run(cls._requeue.pop())
            except IndexError:
                sleep(1.5)
            else:
                cls.item_count -= 1
                sleep(0.1)
