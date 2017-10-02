from enum import Enum

"""
Enumerators for master's commands in TCP json-requests
"""
class Command(Enum):
    REQUEST_PRESENTATION = 0    # for requesting slave's presentation object
    SHOW_NEXT = 1               # for requesting slave to show next element
    INVALID_COMMAND = -1        # for invalid requests

"""
Enumerators for observer notifications
"""
class Notification(Enum):
    CONNECTION_FAILED = -1          # to inform about failed connection
    PRESENTATION_UPDATE = 0         # to inform about updated presentation
    PRESENTATION_STATUS_CHANGE = 1  # to inform about a presentation's status change