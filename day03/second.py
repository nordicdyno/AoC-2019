from first import sections_extract, find_intersections, \
    read_input, direction_deltas, is_horizontal, is_vertical

def find_fewest_combined_steps(w1, w2):
    # print("")

    intersections = all_intersections(w1, w2)
    # print("intersections", intersections)

    d1 = intersection_distances(w1, intersections)
    d2 = intersection_distances(w2, intersections)
    # print("d1:", d1)
    # print("d2:", d2)

    shortest = None
    for i, pair in enumerate(zip(d1, d2)):
        dist = pair[0] + pair[1]
        # print("intersection", i, "sum distance", dist, pair[0], "+", pair[1])
        if shortest is not None and shortest < dist:
            continue
        shortest = dist
    return shortest

def all_intersections(w1, w2):
    h1, v1 = sections_extract(w1)
    h2, v2 = sections_extract(w2)
    found1 = find_intersections(h1, v2)
    found2 = find_intersections(h2, v1)
    return found1 + found2

def intersection_distances(wire, intersections):
    found = [None for _ in intersections]

    # print("intersections", intersections)
    # iX, iY = intersection
    # iX, iY = intersection[0], intersection[1]
    x0, y0 = 0, 0
    distance = 0
    for direction in wire:
        xD, yD, orientation = direction_deltas(direction)
        horizontal = is_horizontal(orientation)

        x1, y1 = x0, y0
        x2, y2 = x0+xD, y0+yD
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1

        # print("step:", [x1, y1], "=>", [x2, y2])

        for n, intersection in enumerate(intersections):
            if found[n] is not None:
                continue
            iX, iY = intersection[0], intersection[1]
            if (horizontal and y1 == iY) and (x1 <= iX <= x2):
                delta = abs(iX - x2)
                if orientation == "R":
                    delta = abs(iX - x1)
                found[n] = distance + delta
                # print("{}: {} += {} => {}".format(orientation, distance, delta, found[n]))
            elif ((not horizontal) and x1 == iX) and (y1 <= iY <= y2):
                delta = abs(iY - y1)
                if orientation == "D":
                    delta = abs(iY - y2)
                found[n] = distance + delta
                # print("V: {} += abs({}-{})->{} => {}".format(distance, y1, iY, abs(y1-iY), found[n]))

        distance += abs(xD)+abs(yD)
        x0, y0 = x0+xD, y0+yD

    return found

if __name__ == "__main__":
    wires = read_input()
    print("result:", find_fewest_combined_steps(wires[0], wires[1]))
