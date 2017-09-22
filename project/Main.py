import sys

from RemuApp import RemuApp

"""
    From main we only all the actual functionality of the app, RemuApp
"""


if __name__ == '__main__':
    args = sys.argv

    address = ''
    master = False

    if len(args) > 1:
        master = args[1] == 'master'
        address = args[2]

    RemuApp().run()
