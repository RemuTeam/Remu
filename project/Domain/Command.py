from enum import IntEnum

"""
Enumerators for master's commands in TCP json-requests
"""
class Command(IntEnum):
    REQUEST_PRESENTATION = 0    # for requesting slave's presentation object
    SHOW_NEXT = 1               # for requesting slave to show next element
    INVALID_COMMAND = -1        # for invalid requests

"""
Enumerators for observer notifications
"""
class Notification(IntEnum):
    CONNECTION_FAILED = -1          # to inform about failed connection
    CONNECTION_ESTABLISHED = 0      # to inform about successful connection
    PRESENTATION_UPDATE = 1         # to inform about updated presentation
    PRESENTATION_STATUS_CHANGE = 2  # to inform about a presentation's status change