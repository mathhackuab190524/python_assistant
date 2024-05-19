def read_file(py_file):
    """
    Reads the content of a Python file.

    This function attempts to read a file specified by `py_file` and return its content.
    If the file is not found, it returns a specific error message.
    If another error occurs, it returns a general error message along with the exception details.

    Parameters:
    py_file (str): The path to the Python file to be read.

    Returns:
    str: The content of the file, or an error message if the file could not be read.
    """
    try:
        with open(py_file, 'r', encoding='utf-8') as f_py:
            return f_py.read()
    except FileNotFoundError:
        return f"Error: The file '{py_file}' was not found."
    except Exception as e:
        return f"Error: An error occurred while reading the file '{py_file}'. Details: {e}"


