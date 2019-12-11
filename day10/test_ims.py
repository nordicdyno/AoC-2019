import ims

def test_ok():
    assert True

def test_parse():
    example_map = [
        ".#..#",
        ".....",
        "#####",
        "....#",
        "...##",
    ]
    expect_arr = [
        [0,1,0,0,1],
        [0,0,0,0,0],
        [1,1,1,1,1],
        [0,0,0,0,1],
        [0,0,0,1,1],
    ]
    m = ims.parse(example_map)
    # print(m)
    assert 5 == len(m) and 5 == len(m[0]), "two dimensional"
    assert expect_arr == m


    # best place: [4][5]
# def test_center_intersections():
#     print()
#     coords = spacemap.parse([
#         ".#..#",
#         ".....",
#         "#####",
#         "....#",
#         "#..##",
#     ])
#     space_map = Map(coords=coords)
#     result = space_map.check_if_visible((1,0), (3,4))
#     # print("result:", result)

#     result = space_map.check_if_visible((0,4), (4,0))
#     # print("result:", result)

#     asteroids = space_map.asteroids()
#     print("Asteroids:", len(asteroids), asteroids)

#     # trace_if_visible((1,0), (3,4))
#     # trace_if_visible((3,4), (1,0))
#     # print("lcm(6,3):", lcm(6,3))
#     # print("lcm(12,6):", lcm(12,6))

def test_find_best_observer_case0():
    # print()
    coords = ims.parse([
        #0123456
        "#.....#",#0
        ".......",#1
        "...#...",#2
        ".......",#3
        "#.....#",#4
    ])
    space_map = ims.Map(coords=coords)
    assert False == space_map.check_if_visible((0,0), (6,4))
    assert True == space_map.check_if_visible((0,0), (6,0))
    # stat = space_map.observerability()
    # print("Observability:",stat)

def test_observability():
    # print()
    coords = ims.parse([
        ".#..#",
        ".....",
        "#####",
        "....#",
        "...##",
    ])
    space_map = ims.Map(coords=coords)
    """
         .7..7
         .....
         67775
         ....7
         ...87
    """
    # p = Point(1, 0)
    observe_expect = {
        (1, 0): 7, (4, 0): 7,
        (0, 2): 6, (1, 2): 7, (2, 2): 7, (3, 2): 7, (4, 2): 5,
        (4, 3): 7,
        (3, 4): 8, (4, 4): 7,
    }
    got = space_map.observerability()
    # print("Got   :", got)
    # print("Expect:", observe_expect)
    assert observe_expect == got

def test_find_best_observer_case1():
    # print()
    coords = ims.parse([
        ".#..#",
        ".....",
        "#####",
        "....#",
        "...##",
    ])
    space_map = ims.Map(coords=coords)
    value, coord = space_map.best_observer()
    # print(value, coord)
    assert 8 == value
    assert (3, 4) == coord

def test_find_best_observer_case2():
    # print()
    coords = ims.parse([
        #0123456789
        "......#.#.",#0 A+2 = 2
        "#..#.#....",#1 A+3 = 5
        "..#######.",#2 A+7 = 12
        ".#.#.###..",#3 A+5 = 17
        ".#..#.....",#4 A+2 = 19
        "..#....#.#",#5 A+3 = 22
        "#..#....#.",#6 A+3 = 25
        ".##.#..###",#7 A+6 = 31
        "##...#..#.",#8 A+4 = 35
        ".#....####",#9 A+5 = 40
    ])
    space_map = ims.Map(coords=coords)
    asteroids = space_map.asteroids()
    assert 40 == len(asteroids)
    value, coord = space_map.best_observer()
    # print(value, coord)


def test_find_best_observer_case3():
    # print()
    coords = ims.parse([
        "#.#...#.#.",
        ".###....#.",
        ".#....#...",
        "##.#.#.#.#",
        "....#.#.#.",
        ".##..###.#",
        "..#...##..",
        "..##....##",
        "......#...",
        ".####.###.",
    ])
    space_map = ims.Map(coords=coords)
    value, coord = space_map.best_observer()
    # print(value, coord)
    assert 35 == value
    assert (1, 2) == coord

def test_find_best_observer_case4():
    # print()
    coords = ims.parse([
        ".#..#..###",
        "####.###.#",
        "....###.#.",
        "..###.##.#",
        "##.##.#.#.",
        "....###..#",
        "..#.#..#.#",
        "#..#.#.###",
        ".##...##.#",
        ".....#.#..",
    ])
    space_map = ims.Map(coords=coords)
    value, coord = space_map.best_observer()
    # print(value, coord)
    assert 41 == value
    assert (6, 3) == coord

def test_find_best_observer_case5():
    # print()
    coords = ims.parse([
        ".#..##.###...#######",
        "##.############..##.",
        ".#.######.########.#",
        ".###.#######.####.#.",
        "#####.##.#.##.###.##",
        "..#####..#.#########",
        "####################",
        "#.####....###.#.#.##",
        "##.#################",
        "#####.##.###..####..",
        "..######..##.#######",
        "####.##.####...##..#",
        ".#####..#.######.###",
        "##...#.##########...",
        "#.##########.#######",
        ".####.#.###.###.#.##",
        "....##.##.###..#####",
        ".#.#.###########.###",
        "#.#.#.#####.####.###",
        "###.##.####.##.#..##",
    ])
    space_map = ims.Map(coords=coords)
    value, coord = space_map.best_observer()
    # print(value, coord)
    assert 210 == value
    assert (11, 13) == coord
