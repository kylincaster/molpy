"""
molpy
========
molpy is a Python package for the creation, manipulation, and study of the
structure, dynamics, and functions of complex molecules.
See https://molpy-roy.readthedocs.io/zh_cn/latest/ for complete documentation.
"""

__version__ = "0.0.1"

# These are import orderwise
from molpy.atom import Atom
from molpy.angle import Angle
from molpy.bond import Bond
from molpy.dihedral import Dihedral
from molpy.group import Group
from molpy.molecule import Molecule
from molpy.forcefield import ForceField
from molpy.system import System
from molpy.cell import Cell
from molpy.ioapi import *
from molpy.algorithms import *
from molpy.neigh import *
from molpy.auto_bonds import *

from molpy.io.xml import read_xml_forcefield
from molpy.forcefield import AtomType, BondType, Template