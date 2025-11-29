def get_file_content(working_directory, file_path):
  print(f"Getting content for file: {file_path} in working directory: {working_directory}")
  print(f"FILE PATH: {file_path}")

  try:
    if file_path not in os.listdir(working_directory):
      return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
  except Exception as e:
    return f'Error: {e}'
    
  try:
    is_file = os.path.isfile(file_path)
  except Exception as e:
    return f'Error: {e}'

  if not is_file:
    return f'Error: File not found or is not a regular file: "{file_path}"'
    
get_file_content("calculator", "main")