from enum import IntEnum


class Command(IntEnum):
    """
    Enumerators for master's commands in TCP json-requests
    """
    REQUEST_PRESENTATION = 0    # for requesting slave's presentation object
    SHOW_NEXT = 1               # for requesting slave to show next element
    END_PRESENTATION = 2        # for requesting slave to end the current presentation
    DROP_CONNECTION = 3         # for informing the slave that the connection is terminated
    INVALID_COMMAND = -1        # for invalid requests
    RETRIEVE_FILES = 4          # for requesting the slave to retrieve files from the master
    SEND_PRESENTATION = 5       # for sending presentation from master to slave


class Notification(IntEnum):
    """
    Enumerators for observer notifications
    """
    CONNECTION_TERMINATED = -2      # to inform about a connection closed on purpose
    CONNECTION_FAILED = -1          # to inform about failed connection
    CONNECTION_ESTABLISHED = 0      # to inform about successful connection
    PRESENTATION_UPDATE = 1         # to inform about updated presentation
    PRESENTATION_STATUS_CHANGE = 2  # to inform about a presentation's status change
    PRESENTATION_ENDED = 3          # to inform about the presentations ending