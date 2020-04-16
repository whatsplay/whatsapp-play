'''
To run tests run
python3 -m unittest discover -s tests
on terminal
'''
#region imports
import unittest
from os import path
from wplay.utils.helpers import log_file_path, logs_path,test_log_file_path, data_folder_path, user_data_folder_path, profile_photos_path, tracking_folder_path
#endregion


#region class
class testPath(unittest.TestCase):

    def test_paths_exist(self):
        self.assertTrue(path.exists(data_folder_path))
        self.assertTrue(path.exists(logs_path))
        self.assertTrue(path.exists(log_file_path))
        self.assertTrue(path.exists(test_log_file_path))
        self.assertTrue(path.exists(user_data_folder_path))
        self.assertTrue(path.exists(profile_photos_path))
        self.assertTrue(path.exists(tracking_folder_path))

if __name__ == '__main__':
	unittest.main()
#endregion