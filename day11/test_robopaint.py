from robopaint import Direction, Rotate, change_direction, move_to_direction


def test_change_direction():
    # "^" + L> => "<"
    assert Direction.Left == change_direction(Direction.Up, Rotate.Left)
    # "^" + R => ">"
    assert Direction.Right == change_direction(Direction.Up, Rotate.Right)

    # "<" + L = "V"
    assert Direction.Down == change_direction(Direction.Left, Rotate.Left)
    # "<" + R = "^"
    assert Direction.Up == change_direction(Direction.Left, Rotate.Right)

    # ">" + L => "^"
    assert Direction.Up == change_direction(Direction.Right, Rotate.Left)
    # ">" + R => "v"
    assert Direction.Down == change_direction(Direction.Right, Rotate.Right)

    # "v" + L -> ">"
    assert Direction.Right == change_direction(Direction.Down, Rotate.Left)
    # "v" + R -> "<"
    assert Direction.Left == change_direction(Direction.Down, Rotate.Right)

def test_move_to_direction():
    p = (3, 3)
    assert (3,4) == move_to_direction(Direction.Down, p)
    assert (3,2) == move_to_direction(Direction.Up, p)
    assert (2,3) == move_to_direction(Direction.Left, p)
    assert (4,3) == move_to_direction(Direction.Right, p)
    # assert (0,1) move_to_direction(Direction.Down)
