buttons = "//Button"
labels = "//Label"

def switch_layout_buttons():
    return layout_buttons("SwitchLayout")

def master_layout_buttons():
    return layout_buttons("MasterGUILayout")

def layout_buttons(layout_name):
    return "//" + layout_name + buttons