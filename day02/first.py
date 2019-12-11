from typing import List, Dict
from pydantic import BaseModel

def add(idx: int, mem: List[int]):
    mem[mem[idx+3]] = mem[mem[idx+1]] + mem[mem[idx+2]]

def mul(idx: int, mem: List[int]):
    mem[mem[idx+3]] = mem[mem[idx+1]] * mem[mem[idx+2]]


opcodes = {1: add, 2: mul}

class CPU(BaseModel):
    # opcodes: Dict
    memory: List[int]

    IP: int = 0 # Instruction Pointer
    step: int = 0
    last_opcode: int = None

    max_steps: int = 100

    def __iter__(self):
        return self

    def __next__(self):
        state = self.state()
        if self.IP > len(self.memory):
            raise StopIteration
        opcode = self.memory[self.IP]
        self.last_opcode = opcode

        if opcode == 99:
            raise StopIteration

        opcodes[opcode](self.IP, self.memory)

        self.IP += 4
        self.step += 1
        return state

    def state(self) -> Dict:
        return {
            "step": self.step,
            "IP": self.IP,
            "last_opcode": self.last_opcode,
        }

    def execute(self):
        for i, _ in enumerate(self):
            if i > self.max_steps:
                raise("Too many steps. Probably program error")



def debug_execute(cpu: CPU):
    print()
    print("initial_state:", cpu.state(), cpu.memory)
    for i, state in enumerate(cpu):
        print(" step:", i)
        print("  state before:", state)
        print("  mem:", cpu.memory)
        print("  state after:", cpu.state())
    print("final_state:", cpu.state(), cpu.memory)

def execute(cpu: CPU):
    for _ in iter(cpu):
        pass


program = [
1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,6,1,19,1,19,5,23,2,10,23,27,2,27,13,31,1,10,31,35,1,35,9,39,2,39,13,43,1,43,5,47,1,47,6,51,2,6,51,55,1,5,55,59,2,9,59,63,2,6,63,67,1,13,67,71,1,9,71,75,2,13,75,79,1,79,10,83,2,83,9,87,1,5,87,91,2,91,6,95,2,13,95,99,1,99,5,103,1,103,2,107,1,107,10,0,99,2,0,14,0
]

if __name__ == "__main__":
    program[1] = 12
    program[2] = 2
    cpu = CPU(memory=program)
    cpu.execute()
    print("[0]", cpu.memory[0])

    # pass
# opcodes = {}
# opcodes[1] = add
# opcodes[2] = mul
