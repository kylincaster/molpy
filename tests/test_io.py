# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-10-22
# version: 0.0.1

import pytest
import networkx as nx
from molpy import fromNetworkXGraph
from molpy import fromASE
import numpy as np

class TestNetworkX:
    def test_from_path_graph(self):
        
        G = fromNetworkXGraph('path_graph', nx.path_graph(10))
        assert G.natoms == 10
        assert G.nbonds == 9
        
    def test_from_cubical_graph(self):
        G = fromNetworkXGraph('cubical_graph', nx.cubical_graph())
        assert G.natoms == 8
        assert G.nbonds == 12
        
    def test_from_complete_graph(self):
        G = fromNetworkXGraph('complete_graph', nx.complete_graph(5))
        assert G.natoms == 5
        assert G.nbonds == 10
        