import os

class PathConstants:
    """
    PathConstants enum encapsulates the paths that are referenced and offers a consistent interface with the paths
    referenced. Paths to often referenced locations (such as the media folder) should be referenced and modified only
    through the PathConstant constants
    """
    TEST_MEDIA_FOLDER = "test_media"
    MEDIA_FOLDER = "media"
    PROJECT_FOLDER = "remuprojects"
    ABSOLUTE_MEDIA_FOLDER = os.path.join(os.getcwd(), MEDIA_FOLDER)
    ABSOLUTE_TEST_MEDIA_FOLDER = os.path.join(os.getcwd(), TEST_MEDIA_FOLDER)
    ABSOLUTE_PROJECT_FOLDER = os.path.join(os.getcwd(), PROJECT_FOLDER)