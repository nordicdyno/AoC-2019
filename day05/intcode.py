from enum import IntEnum
from typing import List, Dict, Callable
from dataclasses import dataclass, field
import functools

# parameter modes:
p_mod = 0 # position mode
i_mod = 1 # immediate mode

class AddrMode(IntEnum):
    POSITION = 0
    IMMEDIATE = 1

# returns opcode & mode flags coded in instruction
def parse_instruction(opcode: int) -> (int, List[int]):
    param_modes = str(opcode)[:-2] or []
    opcode = int(str(opcode)[-2:])
    return opcode, [int(c) for c in reversed(param_modes)]

@dataclass
class Context():
    memory: List[int]
    IP: int = 0
    input: int = None

@dataclass
class OpCode():
    op: Callable
    args_count: int = 0
    def call(self, ctx: Context, parameter_modes: List[int]) -> int:
        op_args = _read_args(ctx, self.args_count, parameter_modes)
        return self.op(ctx, op_args)

def _read_args(ctx: Context, args_count: int, p_modes: List[int]) -> List[int]:
    values = []
    for i in range(args_count):
        v = ctx.memory[ctx.IP+i+1]
        # default mode is the "position mode"
        if (i >= len(p_modes)) or (p_modes[i] == AddrMode.POSITION):
            v = ctx.memory[v]
        values.append(v)
    return values

def op_add(ctx: Context, op_args: List[int]) -> int:
    ip, mem = ctx.IP, ctx.memory
    mem[mem[ip+3]] = functools.reduce(lambda a,b : a+b, op_args)
    return ctx.IP+4

def op_mul(ctx: Context, op_args: List[int]) -> int:
    ip, mem = ctx.IP, ctx.memory
    mem[mem[ip+3]] = functools.reduce(lambda a,b : a*b, op_args)
    return ctx.IP+4

def op_input(ctx: Context, op_args: List[int]) -> int:
    ip, mem = ctx.IP, ctx.memory
    mem[mem[ip+1]] = ctx.input
    # mem[mem[ip+1]] = int(input("input: "))
    return ctx.IP+2

def op_output(ctx: Context, op_args: List[int]) -> int:
    ip, mem = ctx.IP, ctx.memory
    print(mem[mem[ip+1]])
    return ctx.IP+2

def op_jmp_if_true(ctx: Context, op_args: List[int]) -> int:
    if op_args[0]:
        return op_args[1]
    return ctx.IP+3

def op_jmp_if_false(ctx: Context, op_args: List[int]) -> int:
    if op_args[0] == 0:
        return op_args[1]
    return ctx.IP+3

def op_less_than(ctx: Context, op_args: List[int]) -> int:
    ip, mem = ctx.IP, ctx.memory
    value = 1 if op_args[0] < op_args[1] else 0
    mem[mem[ip+3]] = value
    return ctx.IP+4

def op_equals(ctx: Context, op_args: List[int]) -> int:
    ip, mem = ctx.IP, ctx.memory
    value = 1 if op_args[0] == op_args[1] else 0
    mem[mem[ip+3]] = value
    return ctx.IP+4

opcodes = {
    1: OpCode(op_add, 2),
    2: OpCode(op_mul, 2),
    3: OpCode(op_input),
    4: OpCode(op_output),
    5: OpCode(op_jmp_if_true, 2),
    6: OpCode(op_jmp_if_false, 2),
    7: OpCode(op_less_than, 2),
    8: OpCode(op_equals, 2),

    99: OpCode(None),
}

@dataclass
class CPU():
    memory: List[int]
    input: int = None
    max_steps: int = 500

    # execute state
    step: int = field(default=0, init=False)
    last_opcode: int = field(default=None, init=False)
    ctx: Context = field(init=False)

    def __post_init__(self):
        self.ctx = Context(memory=self.memory, input=self.input)

    def __iter__(self):
        return self

    def __next__(self):
        state = self.state()
        if self.ctx.IP > len(self.ctx.memory):
            raise StopIteration

        opcode, raw_modes = parse_instruction(self.ctx.memory[self.ctx.IP])
        self.last_opcode = opcode

        if opcode == 99:
            raise StopIteration

        self.ctx.IP = opcodes[opcode].call(self.ctx, raw_modes)
        self.step += 1
        return state

    def state(self) -> Dict:
        return {
            "step": self.step,
            "IP": self.ctx.IP,
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


def read_file(codefile: str) -> List:
    codes = []
    with open(codefile) as f:
        for line in f:
            if not line:
                continue
            codes.extend([int(x) for x in line.split(",")])
    return codes
