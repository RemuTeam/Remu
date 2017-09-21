import pytest
from tests.GUI.tools import simulate
from tests.GUI.layout_selector import *

from tests.GUI.simulator_fixture import simulator

@pytest.mark.parametrize("params", [{}])
@simulate
def test_master_gui(simulator):

    # widgets are selected with xpath
    simulator.assert_count(switch_layout_buttons(), 2)

    # deep tree goes reversed through the tree
    simulator.assert_text(switch_layout_buttons() + "[1]", "Master")
    simulator.assert_text(switch_layout_buttons() + "[2]", "Slave")

    simulator.tap("//SwitchLayout//Button[1]")

    simulator.assert_count("//MasterGUILayout//Button", 1)

    simulator.assert_text("//MasterGUILayout//Label[3]", "0")

    simulator.tap("//MasterGUILayout//Button[1]")

    simulator.assert_text("//MasterGUILayout//Label[3]", "1")
