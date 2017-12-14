import os
from shutil import copy

# the string to use when prefilling the name for copied file
COPY_EXTENSION = "_copy"


def read_file(filepath):
    """
    Reads a file's content as a string
    :param filepath: the filepath to open
    :return: a string, the file's content
    """
    with open(filepath, "r") as f:
        return f.read()


def read_lines(filepath):
    """
    Reads a file's lines to a list
    :param filepath: a string, the file to open
    :return: a list, the lines of the file
    """
    with open(filepath, "r") as f:
        return f.readlines()


def write_file(path, filename, data):
    """
    Writes a file to the destination given as filename.
    The filename should not contain any directories.
    Creates the path if it doesn't exists
    :param path: a string, the path to write the file to
    :param filename: a string, the filename without a path
    :param data: the data to write
    :return: None
    """
    if check_filename(filename):
        create_directory(path)
        with open(os.path.join(path, filename), "w") as f:
            f.write(data)


def append_to_file(filepath, data):
    """
    Appends the data to a file.
    :param filepath: a string, the file to append the data to
    :param data: the data to append
    :return: None
    """
    with open(filepath, "ab+") as file:
        file.write(data)


def copy_with_overwrite(source, destination):
    """
    Copies the source file to the destination.
    If the destination already exists, overwrites the existing file.
    :param source: a string, the source path
    :param destination: a string, the destination path
    :return: None
    """
    destination_directory_str = os.sep
    destination_directory_str.join(destination.split(os.sep)[:-1])
    create_directory(destination_directory_str)
    copy(source, destination)


def create_directory(path):
    """
    Creates a directory
    :param path: a string, the directory to create
    :return: None
    """
    if not os.path.isdir(path):
        os.mkdir(path)


def prefilled_new_file_name(destination, path):
    """
    Create a prefilled filename based on
    the original destination filename. The filename will differ
    from all the file names currently in the app's media folder
    :param destination: a string, the destination as "path1/path2/filename.ext"
    :return: a string, prefilled filename
    """
    separated_path_list = destination.split(os.sep)
    filename_and_extension = separated_path_list[len(separated_path_list) - 1].split('.')
    filename_copy = ''
    if len(filename_and_extension) > 1:
        filename_copy = create_filename_with_extensions(filename_and_extension, path)
    else:
        filename_copy += filename_and_extension[0] + COPY_EXTENSION
    return filename_copy


def create_filename_with_extensions(filename_and_extensions, path):
    """
    A private helper methos. Creates a file name based on the filename
    and its extensions
    :param filename_and_extensions: a list, first element is the filename, the rest are its extensions
    :return: a string, a filename with extensions
    """
    existing_files = get_filenames_from_path(path)
    extensions = filename_and_extensions[1:]
    filename_with_extensions = filename_and_extensions[0]
    while current_filename_with_extensions(filename_with_extensions, extensions) in existing_files:
        filename_with_extensions += COPY_EXTENSION
    for i in range(len(extensions)):
        filename_with_extensions += '.' + extensions[i]
    return filename_with_extensions


def current_filename_with_extensions(filename, extensions):
    """
    A private helper method. Returns the filename and its extensions.
    :param filename: a string, the file's name
    :param extensions: a list, the extensions
    :return: a string, a filename with extensions
    """
    filename_with_extensions = filename
    for extension in extensions:
        filename_with_extensions += "." + extension
    return filename_with_extensions


def copy_file_as(source, destination):
    """
    Copies the source file to the destination
    :param source: a string, the source file path
    :param destination: a string, the destination path
    :return: None
    """
    copy_with_overwrite(source, destination)


def get_filenames_from_path(path):
    """
    Get all files' names from a path.
    Does not return directories.
    :param path: a string, the path to retrieve the files' names from
    :return: a list
    """
    filenames = [file for file in os.listdir(path) if
                 os.path.isfile(os.path.join(path, file))]
    return filenames


def get_filename_with_extension(filename, extension):
    """
    Get a filename with extension.
    The filename given as parameter may be with or without the extension.
    If the filename doesn't end extension given as parameter, the extension
    is appended to the filename
    :param filename: a string, the filename with or without the extension
    :param extension: a string, the extension to add to the filename
    :return: a string, the filename with the extension
    """
    separated_filename = filename.split(os.sep)[-1]
    separated_extension = separated_filename.split(".")
    if separated_extension is not None and separated_extension[-1] != extension:
        return filename + "." + extension
    return filename


def get_filename_only(filepath):
    """
    Returns the filename from a full path
    :param filepath: a string, the full path of a file
    :return: a string, the filename only
    """
    filename = filepath.split(os.sep)[-1]
    return filename


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
    if not filename.strip() or contains_reserved_chars(filename):
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

def get_type_extension(filename):
    return filename.split('.')[-1]

def absolute_path(directory, file):
    return os.path.join(directory, file)
