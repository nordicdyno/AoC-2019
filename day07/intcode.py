from enum import IntEnum
from typing import List, Dict, Callable, Type
from dataclasses import dataclass, field
import functools


class Interrupt(IntEnum):
    OUTPUT = 4
    HALT = 99

class OutputInt(Exception):
    pass

class HaltInt(Exception):
    pass


@dataclass
class CPU():
    memory: List[int]

    IP: int = 0 # instruction pointer
    last_opcode: int = field(default=None, init=False)

    input: List[int] = field(default_factory=lambda: [])
    INPP: int = 0 # input pointer

    output: List[int]  = field(default_factory=lambda: [])

    max_steps: int = 500

    step: int = field(default=0, init=False)

    last_interrupt: int = field(default=None, init=False)

    def execute_until_interrupt(self):
        try:
            while self.next_op():
                if self.step > self.max_steps:
                    raise("Too many steps. Probably program error")
        except OutputInt as e:
            self.last_interrupt = Interrupt.OUTPUT
        except HaltInt as e:
            # print("HaltInt")
            self.last_interrupt = Interrupt.HALT

    def next_op(self):
        if self.IP > len(self.memory):
            raise("IP is overflow program memory")

        opcode, raw_modes = parse_instruction(self.memory[self.IP])
        self.last_opcode = opcode

        if opcode == 99:
            raise HaltInt()

        self.step += 1
        opcodes[opcode].call(self, raw_modes)
        return True

    def state(self) -> Dict:
        return {
            "step": self.step,
            "IP": self.IP,
            "last_opcode": self.last_opcode,
        }

    def add_input(self, value: int):
        self.input.append(value)

    # def all_output(self):
    #     return self.output

    def last_output(self):
        return self.output[-1]


    def execute(self):
        while True:
            try:
                while self.next_op():
                    if self.step > self.max_steps:
                        raise("Too many steps. Probably program error")
            except OutputInt:
                continue
            except HaltInt:
                pass
            break


# parameter modes:
# p_mod = 0 # position mode
# i_mod = 1 # immediate mode

class AddrMode(IntEnum):
    POSITION = 0
    IMMEDIATE = 1

# returns opcode & mode flags coded in instruction
def parse_instruction(opcode: int) -> (int, List[int]):
    param_modes = str(opcode)[:-2] or []
    opcode = int(str(opcode)[-2:])
    return opcode, [int(c) for c in reversed(param_modes)]

# @dataclass
# class Context():
#     memory: List[int]
#     input: List[int]
#     output: List[int]  = field(default_factory=lambda: [], init=False)
#     IP: int = 0
#     INPP: int = 0 # input pointer


@dataclass
class OpCode():
    op: Callable
    args_count: int = 0
    def call(self, ctx: CPU, parameter_modes: List[int]):
        op_args = _read_args(ctx, self.args_count, parameter_modes)
        self.op(ctx, op_args, )

def _read_args(ctx: CPU, args_count: int, p_modes: List[int]) -> List[int]:
    values = []
    for i in range(args_count):
        v = ctx.memory[ctx.IP+i+1]
        # default mode is the "position mode"
        if (i >= len(p_modes)) or (p_modes[i] == AddrMode.POSITION):
            v = ctx.memory[v]
        values.append(v)
    return values

def op_add(ctx: CPU, op_args: List[int]):
    ip, mem = ctx.IP, ctx.memory
    mem[mem[ip+3]] = functools.reduce(lambda a,b : a+b, op_args)
    ctx.IP += 4

def op_mul(ctx: CPU, op_args: List[int]):
    ip, mem = ctx.IP, ctx.memory
    mem[mem[ip+3]] = functools.reduce(lambda a,b : a*b, op_args)
    ctx.IP += 4

def op_input(ctx: CPU, op_args: List[int]):
    ip, mem = ctx.IP, ctx.memory
    mem[mem[ip+1]] = ctx.input[ctx.INPP]
    ctx.INPP += 1
    ctx.IP += 2

def op_output(ctx: CPU, op_args: List[int]):
    ip, mem = ctx.IP, ctx.memory
    ctx.output.append(mem[mem[ip+1]])
    ctx.IP += 2
    raise OutputInt()

def op_jmp_if_true(ctx: CPU, op_args: List[int]):
    if op_args[0]:
        ctx.IP = op_args[1]
        return
    ctx.IP += 3

def op_jmp_if_false(ctx: CPU, op_args: List[int]):
    ip = 3
    if op_args[0] == 0:
        ctx.IP = op_args[1]
        return
    ctx.IP += 3

def op_less_than(ctx: CPU, op_args: List[int]):
    ip, mem = ctx.IP, ctx.memory
    value = 1 if op_args[0] < op_args[1] else 0
    mem[mem[ip+3]] = value
    ctx.IP += 4

def op_equals(ctx: CPU, op_args: List[int]):
    ip, mem = ctx.IP, ctx.memory
    value = 1 if op_args[0] == op_args[1] else 0
    mem[mem[ip+3]] = value
    ctx.IP += 4

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
