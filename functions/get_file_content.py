import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
  print(f"Getting content for file: {file_path} in working directory: {working_directory}")
  print(f"FILE PATH: {file_path}")

  print(f"LISTING WORKING DIRECTORY CONTENTS: {os.listdir(working_directory)}")

  try:
    if file_path not in os.listdir(working_directory):
      print(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
      return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
  except Exception as e:
    print(f"Error accessing working directory: {e}")
    return f'Error: {e}'  
    
  try:
    file_path = os.path.join(working_directory, file_path)
    is_file = os.path.isfile(file_path)
    print(f"IS FILE: {is_file}")
  except Exception as e:
    return f'Error: {e}'

  if not is_file:
    print(f'Error: File not found or is not a regular file: "{file_path}"')
    return f'Error: File not found or is not a regular file: "{file_path}"'

  try:
    with open(file_path, 'r') as f:
      file_content_string = f.read()
      if len(file_content_string) > MAX_CHARS:
        print(f'{file_content_string[:10000]} [...File "{file_path}" truncated at {MAX_CHARS} characters]')
        return f'{file_content_string[:10000]} [...File "{file_path}" truncated at {MAX_CHARS} characters]'
  except Exception as e:
    print(f"Error reading file: {e}")
    return f'Error: {e}'

get_file_content("calculator", "main.py")