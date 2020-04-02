'''
To run tests run
python3 -m unittest discover -s tests
on terminal
'''
#region imports
import unittest
from os import path
from wplay.utils import Logger
from wplay.utils.helpers import logs_path
#endregion


#region LOGGER create
logger = Logger.setup_logger('logs',logs_path/'logsTest.log')
#endregion


#region class for Logger function
class CaptureLogsExample(unittest.TestCase):

    def test_log_file_exists(self):
        self.assertTrue(path.exists(logs_path/'logsTest.log'))

    def test_assert_logs(self):
        """Verify logs using built-in self.assertLogs()."""
        with self.assertLogs(logger) as logs:
            logger.info("Testing logg class")
        self.assertEqual(logs.output, ['INFO:logs:Testing logg class'])

if __name__ == '__main__':
	unittest.main()
#endregion