#region imports
import os
import signal
import subprocess
import unittest
import psutil 
from wplay.tests import test_func
from wplay.utils import kill_process
#endregion


#region class for test_kill_child_processes function
class Testkill(unittest.TestCase):

    def test_kill(self):
        sproc = test_func.get_test_subprocess()
        test_pid = sproc.pid
        p = psutil.Process(test_pid)
        kill_process.kill_child_processes(test_pid)
        p.wait()
        self.assertFalse(psutil.pid_exists(test_pid))

if __name__ == '__main__':
	unittest.main()
#endregion