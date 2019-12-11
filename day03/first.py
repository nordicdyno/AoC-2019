def direction_deltas(direction) -> (int, int, str):
    d, length = direction[0], int(direction[1:])
    if d == "R":
        return length, 0, d
    if d == "D":
        return 0, -length, d
    if d == "U":
        return 0, +length, d
    if d == "L":
        return -length, 0, d

def is_horizontal(d):
    return d in ["L", "R"]

def is_vertical(d):
    return d in ["U", "D"]


def sections_extract(directions):
    horizontal = []
    vertical = []
    x1, y1 = 0, 0
    for d in directions:
        xD, yD, orientation = direction_deltas(d)
        x2, y2 = x1+xD, y1+yD

        section = [x1, y1, x2, y2]
        # normalize sections (always left->right, down->top)
        if x2 < x1:
            section[0], section[2] = section[2], section[0]
        elif y2 < y1:
            section[1], section[3] = section[3], section[1]
        x1, y1 = x2, y2

        if is_horizontal(orientation):
            horizontal.append(section)
        else:
            vertical.append(section)

    return horizontal, vertical

def find_intersections(horizontal, vertical):
    # print("find_intersections")

    # print("horizontal")
    # for h in horizontal:
    #     print(h)
    # print("vertical")
    # for v in vertical:
    #     print(v)

    intersections = []
    for h in horizontal:
        hY = h[1]
        for v in vertical:
            vX = v[0]
            if (h[0] < vX and h[2] > vX) and (v[1] < hY and v[3] > hY):
                intersections.append([vX, hY])
            # print(v)
    return intersections

def find_closest(w1, w2):
    h1, v1 = sections_extract(w1)
    h2, v2 = sections_extract(w2)
    # intersections =
    found1 = find_intersections(h1, v2)
    found2 = find_intersections(h2, v1)
    closest = None
    for intersection in found1 + found2:
        dist = abs(intersection[0]) + abs(intersection[1])
        # print(intersection, "->", dist)
        if closest and closest < dist:
            continue
        closest = dist
    return closest

def read_input():
    wires = []
    with open('input.txt') as f:
        for line in f:
            if not line:
                continue
            directions = line.split(",")
            wires.append(directions)
    return wires


if __name__ == "__main__":
    wires = read_input()
    print(find_closest(wires[0], wires[1]))
