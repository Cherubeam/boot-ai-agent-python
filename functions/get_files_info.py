import os

def get_files_info(working_directory, directory="."):
  current_directory = False

  if directory == '.':
    full_path = f'../{working_directory}'
    current_directory = True
    print(f'Full path resolved to: {full_path}')
  else:
    try:
      full_path = os.path.join(f'../{working_directory}', directory)
      print(f'Full path resolved to: {full_path}')
    except Exception as e:
      return f'Error: {e}'

  try:
    if directory not in os.listdir(f'../{working_directory}') and not current_directory:
      print(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
      return f'Error: Cannot list "{directory}" as it is outside the permitted working directory' 
  except Exception as e:
    return f'Error: {e}'  

  try:
    is_dir = os.path.isdir(full_path)
    print(f'Is Directory: {is_dir}')
  except Exception as e:
    return f'Error: {e}'

  if not is_dir:
    print(f'Error: "{directory}" is not a directory')
    return f'Error: "{directory}" is not a directory'

  for item in os.listdir(full_path):
    try:
      print(f'- {item}: file_size={os.path.getsize(os.path.join(full_path, item))} bytes, is_dir={os.path.isdir(os.path.join(full_path, item))}')
    except Exception as e:
      return f'Error: {e}'


get_files_info("calculator", ".")