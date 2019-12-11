# import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import first
import itertools

def check_pair(noun, verb):
    cpu = first.CPU(memory=first.program)
    cpu.memory[1] = noun
    cpu.memory[2] = verb
    cpu.execute()
    return cpu.memory[0] == 19690720

if __name__ == "__main__":
    noun, verb = 0, 0
    for noun, verb in itertools.product(range(100), range(100)):
        if check_pair(noun, verb):
            print("FOUND:", noun, verb)
            break
    answer = (100 * noun) + verb
    print("answer:", answer)
    # print("noun:", noun, "verb:", verb)
    # print("[0]    ", cpu.memory[0])

    # for i in range(2**N):
    #     filter

