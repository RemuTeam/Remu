from kivy.config import Config
from screeninfo import get_monitors
import sys

from RemuApp import RemuApp

"""
MAIN MODULE THAT RUNS THE APP

Accepts commandline arguments:
1st argument: if this is 'master', then the app is run
              in master-mode (not implemented)
2nd argument: if this is set, it is considered the
              slave-devices ip-address (not implemented)

"""
if __name__ == '__main__':
    monitor = get_monitors()[0]
    Config.set('graphics', 'fullscreen', '0')
    Config.set('graphics', 'height', str(monitor.height))
    Config.set('graphics', 'width', str(monitor.width))
    Config.set('graphics', 'borderless', '1')
    Config.write()
    args = sys.argv

    address = ''
    master = False

    if len(args) > 1:
        master = args[1] == 'master'

    if len(args) > 2:
        address = args[2]

    RemuApp().run()
