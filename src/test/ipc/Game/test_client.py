from ipc.Game.algorithmBasedClient import *

def test_index_fields():
    c = AlgorithmBasedClient()
    c.index_fields("G G G G C G G G G")
    assert True


