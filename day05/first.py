import intcode

if __name__ == "__main__":
    program = intcode.read_file('code.txt')
    # print(program)
    cpu = intcode.CPU(memory=program, input=1)
    cpu.execute()
    # print("[0]", cpu.memory[0])
