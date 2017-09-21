"""
Helper methods for GUI-testing
"""

# Declare constants:
BUTTONS = "//Button"
LABELS = "//Label"
SWITCH_LAYOUT = "//SwitchLayout"
MASTER_LAYOUT = "//MasterGUILayout"
SLAVE_LAYOUT = "//SlaveGUILayout"


# Generic layout helpers:
def index(i):
    return "[" + str(i) + "]"

def layout_button(layout_name, i):
    return layout_buttons(layout_name) + index(i)

def layout_label(layout_name, i):
    return layout_labels(layout_name) + index(i)

def layout_buttons(layout_name):
    return layout_name + BUTTONS

def layout_labels(layout_name):
    return layout_name + LABELS


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
