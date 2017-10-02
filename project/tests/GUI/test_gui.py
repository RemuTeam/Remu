import pytest
from tests.GUI.tools import simulate
from tests.GUI.layout_selector import *

from tests.GUI.simulator_fixture import simulator


@pytest.mark.parametrize("params", [{}])
@simulate
def test_switch_layout_components(simulator):

    # widgets are selected with xpath
    simulator.assert_count(switch_layout_buttons(), 2)

    # deep tree goes reversed through the tree
    simulator.assert_text(switch_layout_button(1), "Master")
    simulator.assert_text(switch_layout_button(2), "Slave")


@pytest.mark.parametrize("params", [{}])
@simulate
def test_master_button_works(simulator):
    simulator.tap(switch_layout_button(1))

    simulator.assert_text(master_layout_label(2), "Messages sent: ")


@pytest.mark.parametrize("params", [{}])
@simulate
def test_slave_button_works(simulator):
    simulator.tap(switch_layout_button(2))
    simulator.assert_text(slave_layout_label(1), "Currently in slave mode")
    simulator.app.close_connections()

@pytest.mark.parametrize("params", [{}])
@simulate
def test_master_gui(simulator):
    simulator.tap(switch_layout_button(1))

    simulator.assert_count(master_layout_buttons(), 3)

    simulator.tap(master_layout_button(1))

    simulator.assert_text(master_layout_label(3), "1")

@pytest.mark.parametrize("params", [{}])
@simulate
def test_master_gui_components(simulator):
    simulator.tap(switch_layout_button(1))

    simulator.assert_text(master_layout_button(1), "Send message to slave")
    simulator.assert_text(master_layout_button(2), "Back")
    simulator.assert_text(master_layout_button(3), "Add Slave")

@pytest.mark.parametrize("params", [{}])
@simulate
def test_input_stuff(simulator):
    simulator.tap(switch_layout_button(1))
    
    simulator.set_text_to("//MasterGUILayout//TextInput[1]", "100.100.100.100:1000")
    simulator.tap(master_layout_button(3))
    simulator.assert_text(master_layout_label(1), "100.100.100.100:1000")

@pytest.mark.parametrize("params", [{}])
@simulate
def test_slave(simulator):
    simulator.tap(switch_layout_button(2))
    simulator.assert_text(slave_layout_label(1), "Olet slave-näkymässä")
    simulator.tap(slave_layout_button(1))
    simulator.assert_attr(presentation_layout_image(1), "source", None)
    simulator.tap(presentation_layout_button(1))
    simulator.assert_attr(presentation_layout_image(1), "source", "images/a.jpg")
    simulator.tap(presentation_layout_button(1))
    simulator.assert_attr(presentation_layout_image(1), "source", "images/b.jpg")
    simulator.tap(presentation_layout_button(1))
    simulator.assert_text(slave_layout_label(1), "Olet slave-näkymässä")
    simulator.app.close_connections()