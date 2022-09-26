import sys

from dndresmanager.backend import Backend
from dndresmanager.gui import Gui



def main():
    print(sys.argv)
    Gui(backend=Backend(sys.argv[1]))