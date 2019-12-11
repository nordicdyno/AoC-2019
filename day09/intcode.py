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
    code: List[int]
    code_size: int = field(default=0, init=False)
    # _memory: List[int] = field(default_factory=lambda: [0 for _ in range(0, 1000000)])

    IP: int = 0 # instruction pointer
    RBP: int = 0 # relative base pointer
    last_opcode: int = field(default=None, init=False)

    input: List[int] = field(default_factory=lambda: [])
    INPP: int = 0 # input pointer

    output: List[int]  = field(default_factory=lambda: [])

    max_steps: int = 500

    step: int = field(default=0, init=False)

    last_interrupt: int = field(default=None, init=False)

    debug: bool = False

    def __post_init__(self):
        code = self.code
        self.code_size = len(code)
        self.code = [0 for _ in range(0, 1000000)]
        for i, c in enumerate(code):
            self.code[i] = c

    def DBG(self, *args, **argv):
        if not self.debug:
            return
        print(*args, **argv)

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

    def write_memory(self, addr, value):
        self.DBG(f"  W: [{addr}] <- {value}")
        self.code[addr] = value

    def read_memory(self, addr):
        value = self.code[addr]
        if addr < 0:
            raise(f"Address is negative: {addr}!")
        self.DBG(f"  R: [{addr}] -> {value}")
        return value


    def next_op(self):
        if self.IP > len(self.code):
            raise("IP is overflow program memory")

        self.DBG("")
        opcode, raw_modes = parse_instruction(self.code[self.IP])
        self.DBG(f"{self.step+1}: [ ", end='')
        if self.IP > 0:
            self.DBG(f"<...cut {self.IP}...> ", end='')
        for i in range(0, self.code_size):
            c = self.code[i]
            if i < self.IP:
                pass
            elif i == self.IP:
                self.DBG(f"\033[4m{c}\033[0m ", end = '')
            elif i > self.IP+7:
                self.DBG(f"<...cut {self.code_size-i}...> ", end = '')
                break
            else:
                self.DBG(f"{c} ", end = '')

        self.DBG("]")
        self.DBG(f"CODE: {self.code[self.IP]} OP: {opcode}, modes: {raw_modes}")
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
        self.DBG("Code size:", self.code_size)
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


class AddrMode(IntEnum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2

# returns opcode & mode flags coded in instruction
def parse_instruction(opcode: int) -> (int, List[int]):
    params = [int(c) for c in f"{str(opcode)[:-2]:0>5}"[::-1]]
    return int(str(opcode)[-2:]), params

# def debug_print(*args):
#     print(*args)

@dataclass
class OpCode():
    op: Callable
    args_count: int = 0
    last_mem_addr: bool = False
    def call(self, ctx: CPU, parameter_modes: List[int]):
        # print("CALL")
        addr = None
        op_args = _read_args(ctx, self.args_count, parameter_modes)
        if self.last_mem_addr:
            # addr_offset = self.args_count+1
            addr = _read_memory_addr(ctx, self.args_count, parameter_modes[self.args_count])
            # ctx.DBG(f"addr: {addr}")
        self.op(ctx, op_args, addr)

def _read_memory_addr(ctx: CPU, arg_num: int, mode: int) -> int:
    # print(f"ctx.IP+arg_idx -> {ctx.IP}+{arg_num}+1")
    # print(f"mode: {mode}")
    # addr = ctx.IP+arg_idx
    v = ctx.read_memory(ctx.IP+arg_num+1)
    if mode == AddrMode.POSITION:
        # ctx.DBG(f"ADDR: ctx.IP+v")
        return v
    if mode == AddrMode.RELATIVE:
        # v = ctx.read_memory(v)
        ctx.DBG(f"RELATIVE mem: ctx.RBP+value: {ctx.RBP}+{v} -> {ctx.RBP + v}")
        return ctx.RBP + v
    raise("unknown mode for memory parameter")
    # return addr

def _read_args(ctx: CPU, args_count: int, p_modes: List[int]) -> List[int]:
    values = []
    for i in range(args_count):
        v = ctx.code[ctx.IP+i+1] # IMMEDIATE (default)
        mode = p_modes[i]
        ctx.DBG(f" arg [{i}]: {v} ({mode})")

        if mode == AddrMode.POSITION:
            ctx.DBG(f"  abs mem: {v} -> {ctx.code[v]}")
            v = ctx.read_memory(v)
        elif mode == AddrMode.RELATIVE:
            ctx.DBG(f"  rel mem: {ctx.RBP+v} ({ctx.RBP}+{v}) -> {ctx.code[ctx.RBP+v]}")
            v = ctx.read_memory(ctx.RBP+v)
        else:
            ctx.DBG(f"  immediate value: {v}")
        values.append(v)
    return values

def op_add(ctx: CPU, op_args: List[int], addr: int):
    # addr = ctx.code[ctx.IP+3]
    result = functools.reduce(lambda a,b : a+b, op_args)
    ctx.DBG(f"<OP:add> result {result} to address {addr}")
    ctx.write_memory(addr, result)
    ctx.IP += 4

def op_mul(ctx: CPU, op_args: List[int], addr: int):
    # addr = ctx.code[ctx.IP+3]
    result = functools.reduce(lambda a,b : a*b, op_args)
    ctx.DBG(f"<OP:mul> result {result} to address {addr}")
    ctx.write_memory(addr, result)
    ctx.IP += 4

"""
Opcode 3 takes a single integer as input and saves it to the position given by its only parameter.
For example, the instruction 3,50 would take an input value and store it at address 50.
"""
def op_input(ctx: CPU, op_args: List[int], addr: int):
    # value = op_args[0]
    # _read_memory_addr(ctx, 0, addr = ctx.IP + 1
    ctx.DBG(f"<OP:input> write {ctx.input[ctx.INPP]} to address {addr}")
    ctx.write_memory(addr, ctx.input[ctx.INPP])
    ctx.INPP += 1
    ctx.IP += 2

"""
Opcode 4 outputs the value of its only parameter.
For example, the instruction 4,50 would output the value at address 50.
"""
def op_output(ctx: CPU, op_args: List[int], addr: int):
    value = op_args[0]
    ctx.DBG(f"<OP:output> {value}")
    ctx.output.append(value)
    ctx.IP += 2
    raise OutputInt()

"""
jump-if-true

if the first parameter is non-zero, it sets the instruction pointer to the value from the second parameter.
Otherwise, it does nothing.
"""
def op_jmp_if_true(ctx: CPU, op_args: List[int], addr: int):
    ctx.DBG("<OP:jump-if-true>", end='')
    ctx.DBG(f" check {op_args[0]} ", end='')
    if op_args[0]:
        ctx.DBG(f" set IP={op_args[1]}")
        ctx.IP = op_args[1]
        return
    ctx.DBG(f" NOOP")
    ctx.IP += 3

def op_jmp_if_false(ctx: CPU, op_args: List[int], addr: int):
    ctx.DBG("<OP:jump-if-false>", end='')
    ctx.DBG(f" check {op_args[0]} ", end='')
    if op_args[0] == 0:
        ctx.DBG(f" set IP={op_args[1]}")
        ctx.IP = op_args[1]
        return
    ctx.IP += 3

"""
less than: if the first parameter is less than the second parameter, it stores 1
in the position given by the third parameter. Otherwise, it stores 0.
"""
def op_less_than(ctx: CPU, op_args: List[int], addr: int):
    value = 1 if op_args[0] < op_args[1] else 0
    ctx.DBG(f"<OP:less-than> {op_args[0]} < {op_args[1]} -> {value}")

    # addr = ctx.code[ctx.IP+3]
    ctx.write_memory(addr, value)
    ctx.IP += 4

def op_equals(ctx: CPU, op_args: List[int], addr: int):
    value = 1 if op_args[0] == op_args[1] else 0
    ctx.DBG(f"<OP:equals> {op_args[0]} == {op_args[1]} -> {value}")
    ctx.write_memory(addr, value)
    ctx.IP += 4

def op_rbp_set(ctx: CPU, op_args: List[int], addr: int):
    ctx.RBP += op_args[0]
    ctx.IP += 2
    ctx.DBG(f"<OP:RPB-set> RBP={ctx.RBP} (+{op_args[0]})")


opcodes = {
    1: OpCode(op_add, 2, True),
    2: OpCode(op_mul, 2, True),
    3: OpCode(op_input, 0, True),
    4: OpCode(op_output, 1),
    5: OpCode(op_jmp_if_true, 2),
    6: OpCode(op_jmp_if_false, 2),
    7: OpCode(op_less_than, 2, True),
    8: OpCode(op_equals, 2, True),
    9: OpCode(op_rbp_set, 1),

    99: OpCode(None),
}

def read_file(codefile: str) -> List:
    codes = []
    with open(codefile) as f:
        for line in f:
            line = line.split("#")[0].rstrip("\n").replace(" ", "")
            if not line:
                continue
            codes.extend([int(x) for x in line.split(",")])
    return codes
