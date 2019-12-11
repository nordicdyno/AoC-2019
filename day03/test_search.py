from .first import sections_extract, find_intersections, find_closest
from .second import find_fewest_combined_steps

def test_sections_extract():
    print("Extract")
    got1 = sections_extract(["R8","U5","L5","D3"])
    assert [[0, 0, 8, 0], [3, 5, 8, 5]], [[8, 0, 8, 5], [3, 2, 3, 5]] == got1
    # print(got1)
    got2 = sections_extract(["U7","R6","D4","L4"])
    # print(got2)
    assert [[0, 7, 6, 7], [2, 3, 6, 3]], [[0, 0, 0, 7], [6, 3, 6, 7]] == got2

def test_find_intersections():
    h1, v1 = sections_extract(["R8","U5","L5","D3"])
    h2, v2 = sections_extract(["U7","R6","D4","L4"])
    # intersections =
    found1 = find_intersections(h1, v2)
    found2 = find_intersections(h2, v1)
    found = found1 + found2
    found.sort()
    assert [[3,3], [6,5]] == found

def test_find_closest():
    got = find_closest(
        ["R8","U5","L5","D3"],
        ["U7","R6","D4","L4"],
    )
    assert 6 == got

def test_find_fewest_combined_steps_case0():
    w1 = ["R8","U5","L5","D3"]
    w2 = ["U7","R6","D4","L4"]
    got = find_fewest_combined_steps(w1, w2)
    assert 30 == got

def test_find_fewest_combined_steps_case1():
    w1 = ["R75","D30","R83","U83","L12","D49","R71","U7","L72"]
    w2 = ["U62","R66","U55","R34","D71","R55","D58","R83"]
    got = find_fewest_combined_steps(w1, w2)
    assert 610 == got

def test_find_fewest_combined_steps_case2():
    w1 = ["R98","U47","R26","D63","R33","U87","L62","D20","R33","U53","R51"]
    w2 = ["U98","R91","D20","R16","D67","R40","U7","R15","U6","R7"]
    steps = find_fewest_combined_steps(w1, w2)
    assert 410 == steps
