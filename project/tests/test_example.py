import pytest
from tests.tools import simulate

from tests.simulator_fixture import simulator

@pytest.mark.parametrize("params", [{}])
@simulate
def test_example(simulator):

    # widgets are selected with xpath
    simulator.assert_count("//SwitchLayout//Button", 2)

    # deep tree goes reversed through the tree
    simulator.assert_text("//SwitchLayout//Button[1]", "Master")
    simulator.assert_text("//SwitchLayout//Button[2]", "Slave")

    simulator.tap("//SwitchLayout//Button[1]")