"""
Layout selector builds selectors for GUI-testing
"""

# Declare constants:
BUTTONS = "//Button"
LABELS = "//Label"
IMAGES = "//Image"
TEXT_INPUTS = "//TextInput"
SWITCH_LAYOUT = "//SwitchLayout"
MASTER_LAYOUT = "//MasterGUILayout"
SLAVE_LAYOUT = "//SlaveGUILayout"
PRESENTATION_LAYOUT = "//PresentationLayout"
#MASTERBACK_POPUP ="//MasterBackPopUp"

LAYOUTS = [SWITCH_LAYOUT, MASTER_LAYOUT, SLAVE_LAYOUT, PRESENTATION_LAYOUT]#, MASTERBACK_POPUP]
ELEMENTS = [BUTTONS, LABELS, IMAGES, TEXT_INPUTS]


def get_from_layout(layout_name, element, i=None):
    selector = ""
    selector += get_from_constants(layout_name, LAYOUTS)
    selector += get_from_constants(element, ELEMENTS)
    if i is not None:
        selector += index(i)
    return selector


# Helper methods
def get_from_constants(name, list):
    selector = ""
    for value in list:
        if name in value:
            selector = selector + value
    return selector


def index(i):
    return "[" + str(i) + "]"