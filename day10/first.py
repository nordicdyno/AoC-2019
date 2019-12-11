import ims

if __name__ == "__main__":
    amplifiers = []
    coords = ims.read_file('map.txt')
    m = ims.Map(coords=coords)
    value, coord = m.best_observer()

    print(f"value: {value}, coord: {coord}:")
