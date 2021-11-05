# Global Libaries
from enum import auto

# Local Libaries
from FileVariable import FileVariable

# Values
LOW = auto()
HIGH = auto()

# Modes
BCM = auto()
BOARD = auto()

# Setup
IN = auto()
OUT = auto()

fv = FileVariable('./virtualinputs/')


def setmode(mode: auto):
    pass


def cleanup():
    pass


def setup(pin: int, function: auto):
    fv.register_variables([str(pin)])
    fv.write_variable(str(pin), True)


def input(pin: int):
    return fv.read_variable(str(pin))

