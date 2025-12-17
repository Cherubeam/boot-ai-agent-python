import unittest
from functions.run_python_file import run_python_file


class TestRunPythonFile(unittest.TestCase):
    def test_print_calculator_usage_instructions(self):
        result = run_python_file("calculator", "main.py")
        self.assertIn("STDOUT: Calculator App", result)
        self.assertIn('Usage: python main.py "<expression>"', result)
        self.assertIn('Example: python main.py "3 + 5"', result)
        print(result)

    def test_run_calculator(self):
        result = run_python_file("calculator", "main.py", ["3 + 5"])
        self.assertIn('"expression": "3 + 5"', result)
        self.assertIn('"result": 8', result)
        print(result)

    def test_run_calculator_tests(self):
        result = run_python_file("calculator", "tests.py")
        self.assertIn("Ran 9 tests", result)
        self.assertIn("OK", result)
        print(result)

    def test_run_file_outside_working_directory(self):
        result = run_python_file("calculator", "../main.py")
        self.assertIn(
            'Error: Cannot execute "../main.py" as it is outside the permitted working directory',
            result,
        )
        print(result)

    def test_run_non_existent_file(self):
        result = run_python_file("calculator", "nonexistent.py")
        self.assertIn('Error: File "nonexistent.py" not found.', result)
        print(result)

    def test_run_non_python_file(self):
        result = run_python_file("calculator", "lorem.txt")
        self.assertIn('Error: "lorem.txt" is not a Python file.', result)
        print(result)


if __name__ == "__main__":
    unittest.main()
