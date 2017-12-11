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
INFO_LAYOUT = "//InfoLayout"
PRESENTATION_LAYOUT = "//PresentationLayout"
#MASTERBACK_POPUP ="//MasterBackPopUp"

LAYOUTS = [SWITCH_LAYOUT, MASTER_LAYOUT, SLAVE_LAYOUT, INFO_LAYOUT, PRESENTATION_LAYOUT]#, MASTERBACK_POPUP]
ELEMENTS = [BUTTONS, LABELS, IMAGES, TEXT_INPUTS]


def get_from_layout(layout_name, element, additional_selector=None, i=None):
    selector = ""
    selector += get_from_constants(layout_name, LAYOUTS)
    if additional_selector is not None:
        selector += str(additional_selector)
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