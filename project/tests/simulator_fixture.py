import os

import pytest

from project.tests.simulation import Simulator


@pytest.fixture
def simulator(request):
    from project.Main import RemuApp
    application = RemuApp()
    simulator = Simulator(application)
    remu_kv_file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    remu_kv_file_name = "remu.kv"

    def fin():
        simulator.clean_queue()

        from kivy.lang import Builder

        files = list(Builder.files)
        for filename in files:
            Builder.unload_file(filename)
        kivy_style_filename = os.path.join(remu_kv_file_path, remu_kv_file_name)
        if not kivy_style_filename in Builder.files:
            Builder.load_file(kivy_style_filename, rulesonly=False)

    request.addfinalizer(fin)
    return simulator
