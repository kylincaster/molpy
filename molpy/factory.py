# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-10-17
# version: 0.0.1

from typing import Dict
from molpy.atom import Atom
from molpy.group import Group
from molpy.io.pdb import read_pdb
from molpy.io.lmp import write_lmp
import numpy as np
import importlib

from molpy.io.xml import read_xml_forcefield

__all__ = ['path_group']

def full(groupName, atomNames, **properties):
    """ build up a group with atoms

    Args:
        names (List[atomName]): list of atomName to init Atoms
        properties (Dict[str:List]): the len of lists should match with names list
    """
    _atoms = []
    for i, name in enumerate(atomNames):
        atom = Atom(name)
        for k, v in properties.items():
            setattr(atom, k, v[i])
        _atoms.append(atom)
            
    group = Group(groupName)
    for atom in _atoms:
        group.add(atom)
        
    return group

def fromPDB(fpath, index=None):
    with open(fpath, 'r') as f:
        group = read_pdb(f, index=None)
    return group

def fromLAMMPS():
    pass

def fromXML(fpath, type='forcefield'):
    with open(fpath, 'r') as f:
        if type == 'forcefield':
            ff = read_xml_forcefield(f)
            return ff

def toLAMMPS(fpath, system):
    with open(fpath, 'w') as f:
        write_lmp(f, system)