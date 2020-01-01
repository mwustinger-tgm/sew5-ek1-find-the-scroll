from ipc.Game.AlgorithmBasedClient import *
c = AlgorithmBasedClient()
known_spaces = {(0, 0): FieldType.CASTLE, (-1, 1): FieldType.GRASS, (0, 1): FieldType.GRASS, (1, 1): FieldType.GRASS, (-1, 0): FieldType.GRASS, (1, 0): FieldType.GRASS, (-1, -1): FieldType.GRASS, (0, -1): FieldType.GRASS, (1, -1): FieldType.FOREST}
data = "G G G G C G G G F"

def test_move_with_command_UP():
    assert c.move_with_command((0, 0), CommandType.UP) == (0, 1)

def test_move_with_command_DOWN():
    assert c.move_with_command((0, 0), CommandType.DOWN) == (0, -1)

def test_move_with_command_LEFT():
    assert c.move_with_command((0, 0), CommandType.LEFT) == (-1, 0)

def test_move_with_command_RIGHT():
    assert c.move_with_command((0, 0), CommandType.RIGHT) == (1, 0)

def test_index_fields():
    assert c.index_fields({(0, 0): FieldType.CASTLE}, (0, 0), data) == known_spaces

def test_index_fields_with_scroll():
    s = list(data)
    s[1] = 'B'
    c.index_fields({(0, 0): FieldType.CASTLE}, (0, 0), "".join(s))
    assert c.scroll_location == (-1, 1)

def test_is_own_castle_on_own_castle():
    assert c.is_own_castle(known_spaces, (0, 0))

def test_is_own_castle_on_enemy_castle():
    test_spaces = known_spaces
    test_spaces[(1, 0)] = FieldType.CASTLE
    test_spaces[(1, 2)] = FieldType.GRASS
    test_spaces[(0, 2)] = FieldType.GRASS
    test_spaces[(-1, 2)] = FieldType.GRASS
    assert not c.is_own_castle(test_spaces, (0, 1))
