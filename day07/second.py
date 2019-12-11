import intcode
from itertools import permutations, repeat, product
from typing import List, Dict, Callable

def find_best_phase_settings(program: List[int]) -> (int, List[int]):
    phase_settings_values = [i for i in range(5,10)]
    max_value = 0
    best_settings = []
    for phase_settings in permutations(phase_settings_values):
        value = check_phase_settings_loop(program, phase_settings)
        if value < max_value:
            continue
        max_value = value
        best_settings = phase_settings
    return max_value, best_settings

def check_phase_settings_loop(program, phase_settings):
    amplifiers = []
    for i in range(5):
        cpu = intcode.CPU(memory=program.copy(), input=[phase_settings[i]])
        amplifiers.append(cpu)

    last_output = 0
    amplifier_idx = 0
    while True:
        cpu = amplifiers[amplifier_idx]
        # print(f"amplifier {amplifier_idx} last_interrupt {cpu.last_interrupt}")

        if cpu.last_interrupt == intcode.Interrupt.HALT:
            # print(f"amplifier {amplifier_idx} stopped")
            if amplifier_idx == 4:
                break
            else:
                amplifier_idx+=1
                continue


        # print(f"amplifier {amplifier_idx} add_input {last_output}")
        cpu.add_input(last_output)
        cpu.execute_until_interrupt()
        last_output = cpu.last_output()

        if amplifier_idx == 4:
            amplifier_idx = 0
        else:
            amplifier_idx+=1

    return last_output

if __name__ == "__main__":
    amplifiers = []
    program = intcode.read_file('code.txt')

    value, settings = find_best_phase_settings(program)
    print("value:", value, "settings:", settings)
