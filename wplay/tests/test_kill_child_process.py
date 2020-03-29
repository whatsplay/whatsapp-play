#region imports
import os
import signal
import subprocess
import sys
import time
import unittest

import psutil 

from psutil import POSIX

from wplay.tests import test_func
from wplay.utils import kill_process
from wplay.tests import get_test_subprocess
from wplay.tests import PYTHON_EXE
from psutil.tests import retry_on_failure
from psutil.tests import safe_rmpath
from wplay.tests import TESTFILE_PREFIX
from wplay.tests import TESTFN
from wplay.tests import unittest
from wplay.tests import wait_for_pid
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
'''
if __name__ == '__main__':
    from psutil.tests.runner import run
    run(__file__)
'''
#endregion