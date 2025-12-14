import os


def write_file(working_directory, file_path, content):
    absolute_working_dir = os.path.abspath(working_directory)
    absolute_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not absolute_file_path.startswith(absolute_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    try:
        if not os.path.isdir(os.path.dirname(absolute_file_path)):
            os.makedirs(os.path.dirname(absolute_file_path))
    except Exception as e:
        return f'Error creating directories for "{file_path}": {e}'

    try:
        with open(absolute_file_path, "w") as file:
            file.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error writing to file "{file_path}": {e}'


# write_file("calculator", "pkg/new_file.txt", "This is a new file. No, actually, it is just a test.")
