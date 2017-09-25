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
    args = sys.argv

    address = ''
    master = False

    if len(args) > 1:
        master = args[1] == 'master'

    if len(args) > 2:
        address = args[2]

    RemuApp().run()
