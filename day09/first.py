import intcode

if __name__ == "__main__":
    amplifiers = []
    program = intcode.read_file('code.txt')
    cpu = intcode.CPU(code=program, input=[1])
    cpu.debug = True
    cpu.execute()

    print("output:", cpu.output)
