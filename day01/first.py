#!python3
required_fuel = 0
# ship_modules = []
with open('testdata/first-input.txt') as f:
    for line in f:
        if line:
            mass = int(line)
            # print(mass, "/3", mass/3, "//3", mass//3)
            required_fuel += mass//3 - 2
            # ship_modules.append()
# print(ship_modules)
print(required_fuel)
