import intcode

if __name__ == "__main__":
    amplifiers = []
    program = intcode.read_file('code.txt')
    cpu = intcode.CPU(code=program, input=[2], max_steps=1_000_000)
    cpu.execute()

    print("CPU steps:", cpu.step) # 371205 (~40s on MacbookPro 2018)
    print("output:", cpu.output)
