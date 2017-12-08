from Constants.FileHandler import copy_with_overwrite, write_file

import os

# the string to use when prefilling the name for copied file
COPY_EXTENSION = "_copy"


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
    print(existing_files, current_filename_with_extensions(filename_with_extensions, extensions))
    while current_filename_with_extensions(filename_with_extensions, extensions) in existing_files:
        filename_with_extensions += COPY_EXTENSION
    for i in range(len(extensions)):
        filename_with_extensions += '.' + extensions[i]
    return filename_with_extensions


def get_filenames_from_path(path):
    filenames = [file for file in os.listdir(path) if
                 os.path.isfile(os.path.join(path, file))]
    return filenames


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


def create_new_file(self):
    """
    Creates a new file.
    :return: None
    """
    separated_path_list = self.destination_name.split(os.sep)
    separated_path_list[len(separated_path_list) - 1] = self.ids.save_as.text
    file_to_save = separated_path_list[0]
    for i in range(1, len(separated_path_list)):
        file_to_save += os.sep + separated_path_list[i]
    self.copy_file_as(file_to_save)


def copy_file_as(source, destination, path):
    """
    Copies the source file to to another location.
    :param filename: the file to write
    :return: None
    """
    copy_with_overwrite(source, destination)


def save_source_as(data, destination, path):
    write_file(path, destination, data)