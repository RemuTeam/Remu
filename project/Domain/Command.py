from enum import Enum

"""
Enumerators for masters commands in TCP json-requests
"""
class Command(Enum):
    REQUEST_PRESENTATION = 0    # for requesting slave's presentation object
    SHOW_NEXT = 1               # for requesting slave to show next element
