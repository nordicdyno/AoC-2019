import ims

def vaporize_until(m: ims.Map, base: ims.Point, n: int=200) -> ims.Point:
    i = 0
    while m.asteroids():
        for p in m.loop_scan(base_coord):
            m.vaporize(p)
            i += 1
            if i == 200:
                return p
    return None


if __name__ == "__main__":
    amplifiers = []
    coords = ims.read_file('map.txt')
    m = ims.Map(coords=coords)
    value, base_coord = m.best_observer()

    p = vaporize_until(m, base_coord, 200)
    print("200th Point:", p)
    print("x*100 + y =", p[0]*100+p[1])


