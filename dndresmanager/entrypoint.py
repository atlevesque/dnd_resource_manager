import sys

from dndresmanager import Backend, Gui

def main():
    print(sys.argv)
    Gui(backend=Backend("characters/Sopafine.json"))