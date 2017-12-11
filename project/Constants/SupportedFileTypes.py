"""
This file contains information about the
supported file extensions per media type.
"""

ImageFormats = ["*.jpg", "*.png"]
TextFormats = ["*.txt"]
VideoFormats = ["*.mp4"]
AllSupportedFormats = []
AllSupportedFormats.extend(ImageFormats)
AllSupportedFormats.extend(TextFormats)
AllSupportedFormats.extend(VideoFormats)
ProjectFileFormats = ["*.remu"]

def extension_is_supported(ext):
    supported_extensions = [format[2:] for format in AllSupportedFormats]
    print(supported_extensions)
    return ext in supported_extensions