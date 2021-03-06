import os

import pytest

from tests.GUI.simulation import Simulator

@pytest.fixture
def simulator(request):
    from Main import RemuApp
    application = RemuApp()
    simulator = Simulator(application)
    remu_kv_file_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    remu_kv_file_name = 'GUI/remu.kv'

    def fin():
        simulator.clean_queue()

        from kivy.lang import Builder

        files = list(Builder.files)
        for filename in files:
            Builder.unload_file(filename)
        kivy_style_filename = os.path.join(remu_kv_file_path, remu_kv_file_name)
        if not kivy_style_filename in Builder.files:
            Builder.load_file(kivy_style_filename, rulesonly=False)
        application.root.current = 'switch_layout'
        application.close_connections()

    request.addfinalizer(fin)
    return simulator
