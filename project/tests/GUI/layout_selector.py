"""
Helper methods for GUI-testing
"""

# Declare constants:
BUTTONS = "//Button"
LABELS = "//Label"
IMAGES = "//Image"
SWITCH_LAYOUT = "//SwitchLayout"
MASTER_LAYOUT = "//MasterGUILayout"
SLAVE_LAYOUT = "//SlaveGUILayout"
PRESENTATION_LAYOUT = "//PresentationLayout"
#MASTERBACK_POPUP ="//MasterBackPopUp"

# Generic layout helpers:
def index(i):
    return "[" + str(i) + "]"

def layout_button(layout_name, i):
    return layout_buttons(layout_name) + index(i)

def layout_label(layout_name, i):
    return layout_labels(layout_name) + index(i)

def layout_image(layout_name, i):
    return layout_images(layout_name) + index(i)

def layout_buttons(layout_name):
    return layout_name + BUTTONS

def layout_labels(layout_name):
    return layout_name + LABELS

def layout_images(layout_name):
    return layout_name + IMAGES
"""
#Popup general helpers:
def popup_button(popup_name, i):
    return popup_buttons(popup_name) + index(i)

def popup_label(popup_name, i):
    return popup_labels(popup_name) + index(i)

def popup_buttons(popup_name):
    return popup_name + BUTTONS

def popup_labels(popup_name):
    return popup_name + LABELS

"""

# Slave layout helpers:
def slave_layout_buttons():
    return layout_buttons(SLAVE_LAYOUT)

def slave_layout_labels():
    return layout_labels(SLAVE_LAYOUT)

def slave_layout_label(i):
    return layout_label(SLAVE_LAYOUT, i)

def slave_layout_button(i):
    return layout_button(SLAVE_LAYOUT, i)


# Switch layout helpers:
def switch_layout_buttons():
    return layout_buttons(SWITCH_LAYOUT)

def switch_layout_button(i):
    return layout_button(SWITCH_LAYOUT, i)

def switch_layout_label(i):
    return layout_label(SWITCH_LAYOUT, i)

def switch_layout_labels():
    return layout_labels(SWITCH_LAYOUT)


# Master layout helpers:
def master_layout_button(i):
    return layout_button(MASTER_LAYOUT, i)

def master_layout_buttons():
    return layout_buttons(MASTER_LAYOUT)

def master_layout_labels():
    return layout_labels(MASTER_LAYOUT)

def master_layout_label(i):
    return layout_label(MASTER_LAYOUT, i)


# Presentation layout helpers:
def presentation_layout_button(i):
    return layout_button(PRESENTATION_LAYOUT, i)

def presentation_layout_buttons():
    return layout_buttons(PRESENTATION_LAYOUT)

def presentation_layout_image(i):
    return layout_image(PRESENTATION_LAYOUT, i)

def presentation_layout_images():
    return layout_images(PRESENTATION_LAYOUT)
"""
#Master back popup helpers:
def master_back_popup_button(i):
    return popup_button(MASTERBACK_POPUP, i)
def master_back_popup_buttons():
    return popup_buttons(MASTERBACK_POPUP)
def master_back_popup_labels():
    return popup_labels(MASTERBACK_POPUP)
def master_back_popup_label(i):
    return popup_label(MASTERBACK_POPUP,i)
"""