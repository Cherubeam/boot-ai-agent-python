import unittest
from functions.write_file import write_file


class TestWriteFiles(unittest.TestCase):
    def test_write_current_directory(self):
        result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
        self.assertIn(
            'Successfully wrote to "lorem.txt" (28 characters written)', result
        )
        print(result)

    def test_write_subdirectory(self):
        result = write_file(
            "calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"
        )
        self.assertIn(
            'Successfully wrote to "pkg/morelorem.txt" (26 characters written)', result
        )
        print(result)

    def test_write_outside_working_directory(self):
        result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
        self.assertIn(
            'Error: Cannot write to "/tmp/temp.txt" as it is outside the permitted working directory',
            result,
        )
        print(result)


if __name__ == "__main__":
    unittest.main()
