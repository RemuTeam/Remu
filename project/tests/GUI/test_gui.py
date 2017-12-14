import pytest
from tests.GUI.tools import simulate
from tests.GUI.layout_selector import *

from tests.GUI.simulator_fixture import simulator

@pytest.mark.parametrize("params", [{}])
@simulate
def test_switch_layout_components(simulator):

    # widgets are selected with xpath
    simulator.assert_count(get_from_layout("Switch", "Button"), 3)

    # deep tree goes reversed through the tree
    simulator.assert_text(get_from_layout("Switch", "Button", None, 1), "Master")
    simulator.assert_text(get_from_layout("Switch", "Button", None, 2), "Slave")
    simulator.assert_text(get_from_layout("Switch", "Button", None, 3), "Info")

@pytest.mark.parametrize("params", [{}])
@simulate
def test_master_gui_components(simulator):
    simulator.tap(get_from_layout("Switch", "Button", None, 1))
    simulator.assert_text(get_from_layout("Master", "Button", None, 5), "Open files")
    simulator.assert_text(get_from_layout("Master", "Button", None, 6), "New\npresentation")
    simulator.assert_text(get_from_layout("Master", "Button", None, 7), "Remove\npresentations")
    simulator.assert_text(get_from_layout("Master", "Button", "//BottomPanel", 1), "Save project")
    simulator.assert_text(get_from_layout("Master", "Button", "//BottomPanel", 2), "Open project")

@pytest.mark.parametrize("params", [{}])
@simulate
def test_slave_button_works(simulator):
    simulator.tap(get_from_layout("Switch", "Button", None, 2))
    simulator.assert_text(get_from_layout("Slave", "Label", None, 1), "Currently in slave mode")
    simulator.tap(get_from_layout("Slave", "Button", None, 1))

#@pytest.mark.parametrize("params", [{}])
#@simulate
#def test_slave(simulator):
    #simulator.tap(get_from_layout("Switch", "Button", 2))

    #simulator.assert_text(get_from_layout("Slave", "Label", 1), "Currently in slave view")

    #simulator.tap(get_from_layout("Slave", "Button", 1))
    #simulator.assert_attr(get_from_layout("Presentation", "Image", 1), "source", None)

    #simulator.tap(get_from_layout("Slave", "Button", 1))
    #simulator.assert_attr(get_from_layout("Presentation", "Image", 1), "source", "images/a.jpg")

    #simulator.tap(get_from_layout("Presentation", "Button", 1))
    #simulator.assert_attr(get_from_layout("Presentation", "Image", 1), "source", "images/b.jpg")

    #simulator.tap(get_from_layout("Presentation", "Button", 1))
    #simulator.assert_text(get_from_layout("Slave", "Label", 1), "Currently in slave view")

    #simulator.app.close_connections()