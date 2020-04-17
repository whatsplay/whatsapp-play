'''
To run tests run
python3 -m unittest discover -s tests
on terminal
'''
#region imports
import unittest
from wplay.utils.Logger import Logger
from pathlib import Path
#endregion


#region LOGGER create
logger = Logger(Path(__file__).name)
#endregion


#region class for Logger function
class CaptureLogsExample(unittest.TestCase):

    def test_assert_logs(self):
        """Verify logs using built-in self.assertLogs()."""
        logger.error("Testing logg class")
        self.assertTrue(logger, 'test_logger.py - ERROR - Testing logg class')

if __name__ == '__main__':
	unittest.main()
#endregion