import os
from shutil import copy

# the string to use when prefilling the name for copied file
COPY_EXTENSION = "_copy"


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


def prefilled_new_file_name(destination, path):
    """
    A private method to create a prefilled filename based on
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


def copy_file_as(source, destination, path):
    """
    Copies the source file to to another location.
    :param filename: the file to write
    :return: None
    """
    copy_with_overwrite(source, destination)


def save_source_as(data, destination, path):
    write_file(path, destination, data)


def get_filenames_from_path(path):
    filenames = [file for file in os.listdir(path) if
                 os.path.isfile(os.path.join(path, file))]
    return filenames


def get_filename_with_extension(filename, extension):
    separated_filename = filename.split(os.sep)[-1]
    separated_extension = separated_filename.split(".")
    if separated_extension is not None and separated_extension[-1] != extension:
        return filename + "."  + extension
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