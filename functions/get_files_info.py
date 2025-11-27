import os

def get_files_info(working_directory, directory="."):
  current_directory = False

  if directory == '.':
    full_path = working_directory
    current_directory = True
  else:
    try:
      full_path = os.path.join(working_directory, directory)
    except Exception as e:
      return f'Error: {e}'

  try:
    if directory not in os.listdir(working_directory) and not current_directory:
      return f"Result for '{directory}' directory:\nError: Cannot list \"{directory}\" as it is outside the permitted working directory" 
  except Exception as e:
    return f'Error: {e}' 

  try:
    is_dir = os.path.isdir(full_path)
  except Exception as e:
    return f'Error: {e}'

  if not is_dir:
    return f'Error: "{directory}" is not a directory'

  files_info = "Result for current directory:" if current_directory else f"Result for '{directory}' directory:"

  for item in os.listdir(full_path):
    try:
      file_info = f'- {item}: file_size={os.path.getsize(os.path.join(full_path, item))} bytes, is_dir={os.path.isdir(os.path.join(full_path, item))}'
      files_info = '\n'.join((files_info, file_info))
    except Exception as e:
      return f'Error: {e}'
  
  return files_info