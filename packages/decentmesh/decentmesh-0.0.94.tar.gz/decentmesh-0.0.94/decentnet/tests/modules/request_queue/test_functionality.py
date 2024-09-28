import time
import unittest
from threading import Thread

from decentnet.consensus.metrics_constants import MAX_REQUEST_QUEUE_LEN
from decentnet.modules.req_queue.reques_queue import ReqQueue


class TestReqQueue(unittest.TestCase):

    def setUp(self):
        ReqQueue.init_queue()  # Initialize the queue before each test
        ReqQueue.item_count = 0

    def test_append_function_to_queue_with_modified_len(self):
        # Test with modified queue length
        def test_func():
            pass

        # Test appending the function to the queue
        ReqQueue.append(test_func)
        ReqQueue.append(test_func)

        # Attempt to add another function, which should not append immediately

        # Verify the length and item count in the queue
        self.assertEqual(len(ReqQueue._requeue), 2)
        self.assertEqual(ReqQueue.item_count, 2)

    def test_wait_when_queue_full_with_modified_len(self):
        # Test with modified queue length
        async def test_func():
            pass

        # Fill the queue to its maximum length (2 in this case)
        for _ in range(MAX_REQUEST_QUEUE_LEN):
            ReqQueue.append(test_func())

        # Check queue length before adding one more function
        self.assertEqual(len(ReqQueue._requeue), MAX_REQUEST_QUEUE_LEN)
        self.assertEqual(ReqQueue.item_count, MAX_REQUEST_QUEUE_LEN)

        def delayed_start():
            time.sleep(1)
            ReqQueue.do_requests(False)

        Thread(target=delayed_start, daemon=True).start()

        start_time = time.time()
        ReqQueue.append(test_func())
        end_time = time.time()

        if end_time - start_time < 1:
            self.fail("Did not wait for queue to empty")


if __name__ == '__main__':
    unittest.main()
