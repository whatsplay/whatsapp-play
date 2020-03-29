import multiprocessing
import unittest
import os
import time
import psutil 
import signal
from psutil import POSIX
from wplay.utils import kill_process

class Testkill(unittest.TestCase):

    def test_kill(self):
        sproc = l.get_test_subprocess()
        test_pid = sproc.pid
        p = psutil.Process(test_pid)
        kill_process.kill_child_processes(test_pid)
        p.wait()
        self.assertFalse(psutil.pid_exists(test_pid))

if __name__ == '__main__':
	unittest.main()
'''
if __name__ == '__main__':
    from psutil.tests.runner import run
    run(__file__)
'''