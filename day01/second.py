#!python3

def extra_fuel(amount):
    extra = 0
    while amount > 0:
        extra += amount
        amount = amount//3 - 2
    return extra

def module_fuel(mass):
    fuel = 0
    extra_fuel = mass//3 - 2
    while extra_fuel > 0:
        fuel += extra_fuel
        extra_fuel = extra_fuel//3 - 2
    return fuel

def calc_fuel(modules):
    fuel = 0
    for mass in modules:
        # print("Module with mass", mass, "fuel:", module_fuel(mass))
        fuel += module_fuel(mass)
    return fuel



def print_solution():
    ship_modules = []
    with open('testdata/first-input.txt') as f:
        for line in f:
            if line:
                mass = int(line)
                ship_modules.append(mass)
    all_fuel = calc_fuel(ship_modules)
    print(all_fuel)
