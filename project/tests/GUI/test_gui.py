import pytest
from tests.GUI.tools import simulate
from tests.GUI.layout_selector import *

from tests.GUI.simulator_fixture import simulator

@pytest.mark.parametrize("params", [{}])
@simulate
def test_switch_layout_components(simulator):

    # widgets are selected with xpath
    simulator.assert_count(get_from_layout("Switch", "Button"), 2)

    # deep tree goes reversed through the tree
    simulator.assert_text(get_from_layout("Switch", "Button", 1), "Master")
    simulator.assert_text(get_from_layout("Switch", "Button", 2), "Slave")


@pytest.mark.parametrize("params", [{}])
@simulate
def test_master_button_works(simulator):
    simulator.tap(get_from_layout("Switch", "Button", 1))

    simulator.assert_text(get_from_layout("Master", "Label", 2), "Messages sent: ")


@pytest.mark.parametrize("params", [{}])
@simulate
def test_slave_button_works(simulator):
    simulator.tap(get_from_layout("Switch", "Button", 2))
    simulator.assert_text(get_from_layout("Slave", "Label", 1), "Currently in slave mode")
    simulator.app.close_connections()

@pytest.mark.parametrize("params", [{}])
@simulate
def test_master_gui(simulator):
    simulator.tap(get_from_layout("Switch", "Button", 1))

    simulator.assert_count(get_from_layout("Master", "Button"), 3)
    simulator.tap(get_from_layout("Master", "Button", 1))
    simulator.assert_text(get_from_layout("Master", "Label", 3), "1")

@pytest.mark.parametrize("params", [{}])
@simulate
def test_master_gui_components(simulator):
    simulator.tap(get_from_layout("Switch", "Button", 1))

    simulator.assert_text(get_from_layout("Master", "Button", 1), "Send message to slave")
    simulator.assert_text(get_from_layout("Master", "Button", 2), "Back")
    simulator.assert_text(get_from_layout("Master", "Button", 3), "Add Slave")

@pytest.mark.parametrize("params", [{}])
@simulate
def test_ip_changes_when_pressed(simulator):
    simulator.tap(get_from_layout("Switch", "Button", 1))

    simulator.set_text_to(get_from_layout("Master", "TextInput", 1), "100.100.100.100:1000")
    simulator.tap(get_from_layout("Master", "Button", 3))
    simulator.assert_text(get_from_layout("Master", "Label", 1), "100.100.100.100:1000")

@pytest.mark.parametrize("params", [{}])
@simulate
def test_slave(simulator):
    simulator.tap(get_from_layout("Switch", "Button", 2))

    simulator.assert_text(get_from_layout("Slave", "Label", 1), "Currently in slave view")

    simulator.tap(get_from_layout("Slave", "Button", 1))
    simulator.assert_attr(get_from_layout("Presentation", "Image", 1), "source", None)

    simulator.tap(get_from_layout("Slave", "Button", 1))
    simulator.assert_attr(get_from_layout("Presentation", "Image", 1), "source", "images/a.jpg")

    simulator.tap(get_from_layout("Presentation", "Button", 1))
    simulator.assert_attr(get_from_layout("Presentation", "Image", 1), "source", "images/b.jpg")

    simulator.tap(get_from_layout("Presentation", "Button", 1))
    simulator.assert_text(get_from_layout("Slave", "Label", 1), "Currently in slave view")

    simulator.app.close_connections()