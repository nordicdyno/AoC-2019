import ims
import math
# from typing import List, Dict, Callable, Type, Iterable, Tuple

# Point = Tuple[int, int]


def test_rotate_1():
    print()
    map_data = [
        #01234567890123456
        ".#....#####...#..", # 0
        "##...##.#####..##", # 1
        "##...#...#.#####.", # 2
        "..#.....X...###..", # 3 X=(8,3)
        "..#.#.....#....##", # 4
    ]
    coords = ims.parse(map_data)
    m = ims.Map(coords=coords)
    X = (8,3)

    expect_loop1 = [
         (8, 1),  (9, 0),  (9, 1), (10, 0),  (9, 2), (11, 1), (12, 1), (11, 2), (15, 1),
        (12, 2), (13, 2), (14, 2), (15, 2), (12, 3), (16, 4), (15, 4), (10, 4),  (4, 4),
         (2, 4),  (2, 3),  (0, 2),  (1, 2),  (0, 1),  (1, 1),  (5, 2),  (1, 0),  (5, 1),
         (6, 1), (6, 0), (7, 0),
    ]
    loop1 = [p for p in m.loop_scan(X)]
    assert expect_loop1 == loop1

    print("INITIAL STATE")
    print(m)
    for p in m.loop_scan(X):
        m.vaporize(p)
    print("AFTER 1st LOOP VAPORATION")
    print(m)
