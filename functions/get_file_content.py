import os
import sys
from pathlib import Path
from config import MAX_CHARS

sys.path.insert(0, str(Path(__file__).parent.parent))

def get_file_content(working_directory, file_path):
  absolute_working_dir = os.path.abspath(working_directory)
  target_dir = os.path.abspath(os.path.join(working_directory, file_path))

  try:
    if not target_dir.startswith(absolute_working_dir):
      return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
  except Exception as e:
    return f'Error: {e}'  
    
  try:
    is_file = os.path.isfile(target_dir)
  except Exception as e:
    return f'Error: {e}'

  if not is_file:
    return f'Error: File not found or is not a regular file: "{target_dir}"'

  try:
    with open(target_dir, 'r') as f:
      file_content_string = f.read()
      if len(file_content_string) > MAX_CHARS:
        return f'{file_content_string[:10000]} [...File "{os.path.join(working_directory, file_path)}" truncated at {MAX_CHARS} characters]'
      return file_content_string
  except Exception as e:
    return f'Error: {e}'
