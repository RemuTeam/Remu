import os

def read_file(filename):
    with open(filename, "r") as f:
        return f.read()

def read_lines(filename):
    with open(filename, "r") as f:
        return f.readlines()

def write_file(path, filename, data):
    if check_filename(filename):
        with open(os.path.join(path, filename), "w") as f:
            f.write(data)


"""
This list contains all characters that are reserved when naming a file
either in Unix or Windows
"""
ReservedFilenameChars = ["/", "\\", "?", "%", "*", ":", "|", '"', "<", ">"]

def check_filename(filename):
    """
    A static method to check whether filename is valid
    :param filename: a string, the filename to check
    :return: True if valid, False otherwise
    """
    if not filename or contains_reserved_chars(filename):
        return False
    else:
        return True

def contains_reserved_chars(filename):
    """
    Checks whether the filename contains OS-reserved characters
    :param filename: the filename to check
    :return: True if contains reserved characters, False otherwise
    """
    for reserved_char in ReservedFilenameChars:
        if reserved_char in filename:
            return True

    return False