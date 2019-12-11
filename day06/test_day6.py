import functools
from dataclasses import dataclass, field
from collections import defaultdict
from typing import Type, List, Dict

def read_coded_orbits(data: List) -> Dict:
    orbits = {}
    for coded_orbit in data:
        parent_name, name = coded_orbit.split(")")
        orbits[name] = parent_name
    return orbits

def read_file(orbitfile: str) -> Dict:
    coded_orbits = []
    with open(orbitfile) as f:
        for line in f:
            if not line:
                continue
            coded_orbits.append(line.rstrip())
    return read_coded_orbits(coded_orbits)

def make_orbiters(orbits: Dict) -> Dict:
    orbiters = defaultdict(list)
    for name, p_name in orbits.items():
        orbiters[name].append(name)
        while p_name != "COM":
            orbiters[name].append(p_name)
            p_name = orbits[p_name]
    return orbiters

def calc_depth(orbits: Dict) -> int:
    orbiters = make_orbiters(orbits)
    return functools.reduce(lambda a,b : a+b, [len(orbiters[x]) for x in orbiters])


# second part

@dataclass
class orbitItem():
    name: str
    parent: Type['orbitItem'] = None

def find_path_len(orbits: Dict, _from: str, _to: str) -> int:
    orbitree= {"COM": orbitItem("COM")}
    for name in orbits:
        orbitree[name] = orbitItem(name)
    for name, p_name in orbits.items():
        orbitree[name].parent = orbitree[p_name]

    # find common parent
    # save distance while traverse parents
    node = orbitree[_from]
    seen = {}
    depth = 0
    while node.parent != None:
        node = node.parent
        seen[node.name] = depth
        depth += 1

    node = orbitree[_to]
    depth = 0
    while node.parent != None:
        node = node.parent
        if seen.get(node.name):
            return depth + seen[node.name]
        depth += 1

    return None

###########################################################################

def test_data():
    orbits = read_coded_orbits([
        "COM)B", "B)C", "C)D", "D)E", "E)F", "B)G", "G)H", "D)I", "E)J", "J)K", "K)L"
    ])
    assert 42 == calc_depth(orbits)

# solution1
def test_input_data_depth():
    orbits = read_file("input.txt")
    assert 200001 == calc_depth(orbits)

def test_path_len():
    orbits = read_coded_orbits(
        ["COM)B", "B)C", "C)D", "D)E", "E)F", "B)G", "G)H", "D)I", "E)J", "J)K", "K)L", "K)YOU", "I)SAN"]
    )
    assert 4 == find_path_len(orbits, "YOU", "SAN")

# solution2
def test_input_path_len():
    orbits = read_file("input.txt")
    assert 379 == find_path_len(orbits, "YOU", "SAN")
