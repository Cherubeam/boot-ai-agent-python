import unittest
import re
from functions.get_file_content import get_file_content

class TestGetFilesContent(unittest.TestCase):
  def test_content_truncation(self):
    result = get_file_content("calculator", "lorem.txt")
    self.assertTrue(result.startswith("Lorem Ipsum"))
    self.assertIn('[...File "calculator/lorem.txt" truncated at', result)
    print(result)


if __name__ == "__main__":
    unittest.main()