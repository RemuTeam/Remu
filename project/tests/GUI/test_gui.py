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
def test_master_gui_components(simulator):
    simulator.tap(get_from_layout("Switch", "Button", 1))

    simulator.assert_text(get_from_layout("Master", "Button", 1), "Start presentation")
    simulator.assert_text(get_from_layout("Master", "Button", 2), "show next")
    simulator.assert_text(get_from_layout("Master", "Button", 3), "Back")

@pytest.mark.parametrize("params", [{}])
@simulate
def test_slave_button_works(simulator):
    simulator.tap(get_from_layout("Switch", "Button", 2))
    simulator.assert_text(get_from_layout("Slave", "Label", 1), "Currently in slave mode")

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

#@pytest.mark.parametrize("params", [{}])
#@simulate
#def test_MasterBackPopup(simulator):
 #   simulator.tap(switch_layout_button(1))
 #   simulator.tap(master_layout_button(2))
    #simulator.assert_count(master_back_popup_buttons(),2)
    #simulator.assert_count(master_back_popup_labels(),1)
    #simulator.tap(master_back_popup_button(1))
    #simulator.assert_text(switch_layout_button(1),"Master")