import sys

from RemuApp import RemuApp

if __name__ == '__main__':
    args = sys.argv

    address = ''
    master = False

    if len(args) > 1:
        master = args[1] == 'master'
        address = args[2]

    RemuApp().run()
