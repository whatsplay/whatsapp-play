'''
To run tests run
python3 -m unittest discover -s tests
on terminal
'''
#region imports
import unittest
from os import path
from wplay.utils.Logger import Logger
from pathlib import Path
from wplay.utils.helpers import log_file_path
#endregion


#region LOGGER create
him = Logger(Path(__file__).name)
#endregion

tim=str(him)

#region class for Logger function
class TestLogging(unittest.TestCase):

    def test_log_file_exists(self):
        self.assertTrue(path.exists(log_file_path))

    def test_assert_logs(self):
        """Verify logs using built-in self.assertLogs()."""
        him.debug('Getting open pages')
        #with self.assertLogs(him) as logs:
            #him.debug('Getting open pages')
        self.assertLogs(him)
        self.assertEqual(tim, ['DEBUG Getting open pages'])

if __name__ == '__main__':
	unittest.main()
#endregion