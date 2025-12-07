import unittest
import re
from functions.get_files_info import get_files_info

class TestGetFilesInfo(unittest.TestCase):
  def test_current_directory(self):
    result = get_files_info("calculator", ".")

    self.assertTrue(result.startswith("Result for current directory:"))
    self.assertIsNotNone(re.search(r'- main\.py: file_size=\d+ bytes, is_dir=False', result))
    self.assertIsNotNone(re.search(r'- tests\.py: file_size=\d+ bytes, is_dir=False', result))
    self.assertIsNotNone(re.search(r'- pkg: file_size=\d+ bytes, is_dir=True', result))
    print(result)

  def test_pkg_directory(self):
    result = get_files_info("calculator", "pkg")

    self.assertTrue(result.startswith("Result for 'pkg' directory:"))
    self.assertIsNotNone(re.search(r'- calculator\.py: file_size=\d+ bytes, is_dir=False', result))
    self.assertIsNotNone(re.search(r'- render\.py: file_size=\d+ bytes, is_dir=False', result))
    print(result)

  def test_non_existent_directory(self):
    result = get_files_info("calculator", "/bin")

    self.assertTrue(result.startswith("Result for '/bin' directory:"))
    self.assertIn('Error: Cannot list "/bin" as it is outside the permitted working directory', result)
    print(result)

  def test_outside_working_directory(self):
    result = get_files_info("calculator", "../")

    self.assertTrue(result.startswith("Result for '../' directory:"))
    self.assertIn('Error: Cannot list "../" as it is outside the permitted working directory', result)
    print(result)

if __name__ == "__main__":
    unittest.main()