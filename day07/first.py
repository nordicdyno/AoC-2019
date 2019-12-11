import intcode
from itertools import permutations, repeat, product
from typing import List, Dict, Callable

def find_best_phase_settings(program: List[int]) -> (int, List[int]):
    phase_settings_values = [i for i in range(5)]
    max_value = 0
    best_settings = []
    for phase_settings in permutations(phase_settings_values):
        value = check_phase_settings(program, phase_settings)
        if value < max_value:
            continue
        max_value = value
        best_settings = phase_settings
    return max_value, best_settings

def check_phase_settings(program, phase_settings):
    last_output = 0
    for i in range(5):
        cpu = intcode.CPU(memory=program.copy(), input=[phase_settings[i], last_output])
        cpu.execute()
        last_output = cpu.last_output()
    return last_output

if __name__ == "__main__":
    amplifiers = []
    program = intcode.read_file('code.txt')

    value, settings = find_best_phase_settings(program)
    print("value:", value, "settings:", settings)

    # for phase_settings in product(range(5), repeat=5):
    #     print(phase_settings)

    # for phase in permutations(phase_settings)

    # for i in range(5):
    #     # print(i)
    #     phase_settings.append(0)

    #     for j in range(5):
    #         print(i,j)

    # print(program)
        # amplifiers.append(intcode.CPU(memory=program.copy(), input=prog_input))
        # cpu.execute()
    # print("[0]", cpu.memory[0])
