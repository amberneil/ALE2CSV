import unittest
from unittest.mock import MagicMock, patch
from main import read_file_to_string


# Mock the built-in open() context manager.
mock_open = MagicMock(name='mock_open')
mock_open.return_value = MagicMock(name='mock_file_object')
mock_open.return_value.__enter__ = MagicMock(name='mock_enter')
mock_open.return_value.__enter__.return_value = MagicMock(name='mock_enter_return')
mock_open.return_value.__enter__.return_value.read = MagicMock(name='mock_read')
mock_open.return_value.__enter__.return_value.read.return_value = "s"



@patch('main.open', mock_open)
class MainTest(unittest.TestCase):

    @patch('main.os.path.exists', return_value=True)        
    def test_read_file_returns_str(self, mock_os_path_exists):    
        self.assertIsInstance(read_file_to_string('anypath'), str)
    
    def test_read_file_fails_on_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            read_file_to_string('not_a_path')
    
    def can_parse_ale_string(self):
        pass

    



if __name__ == '__main__':
    unittest.main()