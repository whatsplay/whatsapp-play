'''
To run tests run
python3 -m unittest discover -s tests
on terminal
'''
#region imports
import unittest
from os import path
from wplay.utils import helpers
#endregion


#region class
class testPath(unittest.TestCase):

    def test_paths_exist(self):
        # self.assertTrue(path.exists(helpers.audio_file_folder_path))
        # self.assertTrue(path.exists(helpers.chatbot_image_folder_path))
        self.assertTrue(path.exists(helpers.data_folder_path))
        self.assertTrue(path.exists(helpers.logs_path))
        self.assertTrue(path.exists(helpers.log_file_path))
        # self.assertTrue(path.exists(helpers.media_path))
        # self.assertTrue(path.exists(helpers.messages_json_folder_path))
        # self.assertTrue(path.exists(helpers.messages_json_path))
        # self.assertTrue(path.exists(helpers.open_messages_json_path))
        # self.assertTrue(path.exists(helpers.profile_photos_path))
        # self.assertTrue(path.exists(helpers.save_chat_folder_path))
        self.assertTrue(path.exists(helpers.test_log_file_path))
        # self.assertTrue(path.exists(helpers.tracking_folder_path))
        # self.assertTrue(path.exists(helpers.user_data_folder_path))

if __name__ == '__main__':
	unittest.main()
#endregion
