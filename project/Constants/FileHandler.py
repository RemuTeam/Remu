import os
from shutil import copy


def read_file(filename):
    with open(filename, "r") as f:
        return f.read()


def read_lines(filename):
    with open(filename, "r") as f:
        return f.readlines()


def write_file(path, filename, data):
    if check_filename(filename):
        create_directory(path)
        with open(os.path.join(path, filename), "w") as f:
            f.write(data)


def copy_with_overwrite(source, destination):
    print("dest dir:""source:", source, "destination:", destination)
    destination_directory_str = os.sep
    destination_directory_str.join(destination.split(os.sep)[:-1])
    print(destination_directory_str)
    create_directory(destination_directory_str)
    copy(source, destination)


def create_directory(path):
    if not os.path.isdir(path):
        os.mkdir(path)


def get_filename_with_extension(filename, extension):
    separated_filename = filename.split(os.sep)[-1]
    separated_extension = separated_filename.split(".")


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