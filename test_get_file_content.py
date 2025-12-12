import unittest
import re
from functions.get_file_content import get_file_content


class TestGetFilesContent(unittest.TestCase):
    def test_content_truncation(self):
        result = get_file_content("calculator", "lorem.txt")
        self.assertTrue(result.startswith("Lorem Ipsum"))
        self.assertIn('[...File "calculator/lorem.txt" truncated at', result)

    def test_file_content_current_directory(self):
        result = get_file_content("calculator", "main.py")
        self.assertIn("def main():", result)
        print(result)

    def test_file_content_subdirectory(self):
        result = get_file_content("calculator", "pkg/calculator.py")
        self.assertIn("class Calculator:", result)
        print(result)

    def test_non_existent_directory(self):
        result = get_file_content("calculator", "/bin/cat")
        self.assertIn(
            'Error: Cannot read "/bin/cat" as it is outside the permitted working directory',
            result,
        )
        print(result)

    def test_non_existing_file(self):
        result = get_file_content("calculator", "pkg/does_not_exist.py")
        self.assertIn("Error: File not found or is not a regular file:", result)
        print(result)


if __name__ == "__main__":
    unittest.main()
