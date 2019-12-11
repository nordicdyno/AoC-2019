from . import intcode

def test_parse_opcode_1():
    code, modes = intcode.parse_instruction(1)
    assert 1 == code
    assert [] == modes

    code, modes = intcode.parse_instruction(101)
    assert 1 == code
    assert [1] == modes

    code, modes = intcode.parse_instruction(10001)
    assert 1 == code
    assert [0,0,1] == modes


def test_parse_opcode_2():
    code, modes = intcode.parse_instruction(2)
    assert 2 == code
    assert [] == modes

    code, modes = intcode.parse_instruction(1002)
    assert 2 == code
    assert [0,1] == modes

def test_parse_opcode_3():
    code, modes = intcode.parse_instruction(3)
    assert 3 == code
    assert [] == modes


def test_parse_opcode_4():
    code, modes = intcode.parse_instruction(4)
    assert 4 == code
    assert [] == modes

    code, modes = intcode.parse_instruction(104)
    assert 4 == code
    assert [1] == modes


def test_parse_opcode_99():
    code, modes = intcode.parse_instruction(99)
    assert 99 == code
    assert [] == modes


def test_add():
    mem    = [1,9,10,3,  2,3,11,0, 99,30,40,50]
    expect = [1,9,10,30+40, 2,3,11,0, 99,30,40,50]
    add = intcode.OpCode(intcode.op_add, 2)
    _, raw_modes = intcode.parse_instruction(mem[0])
    add.call(intcode.CPU(memory=mem), raw_modes)
    assert mem == expect

def test_mul():
    mem    = [1,9,10,3,  2,3,11,0, 99,30,40,50]
    expect = [1,9,10,30*40, 2,3,11,0, 99,30,40,50]
    mul = intcode.OpCode(intcode.op_mul, 2)
    _, raw_modes = intcode.parse_instruction(mem[0])
    mul.call(intcode.CPU(memory=mem), raw_modes)
    assert mem == expect

def test_cpu_init():
    mem    =  [1,9,10,3,  2,3,11,0, 99,30,40,50]
    cpu = intcode.CPU(memory=mem)
    assert 0 == cpu.IP
    assert mem == cpu.memory

def test_enum_values():
    assert 0 == intcode.AddrMode.POSITION
    assert 1 == intcode.AddrMode.IMMEDIATE

def test_run_sample0():
    mem    =  [1,9,10,3,  2,3,11,0, 99,30,40,50]
    expect = [3500,9,10,70, 2,3,11,0, 99,30,40,50]
    cpu = intcode.CPU(memory=mem)
    cpu.execute()
    assert mem == expect

def test_run_sample1():
    mem = [1,0,0,0,99]
    becomes = [2,0,0,0,99] # (1 + 1 = 2).
    cpu = intcode.CPU(memory=mem)
    cpu.execute()
    assert mem == becomes

def test_run_sample2():
    mem = [2,3,0,3,99]
    becomes = [2,3,0,6,99] # (3 * 2 = 6).
    cpu = intcode.CPU(memory=mem)
    cpu.execute()
    assert mem == becomes

def test_run_sample3():
    mem = [2,4,4,5,99,0]
    becomes = [2,4,4,5,99,9801] # (99 * 99 = 9801).
    cpu = intcode.CPU(memory=mem)
    cpu.execute()
    assert mem == becomes

def test_run_sample4():
    mem = [1,1,1,4,99,5,6,0,99]
    becomes = [30,1,1,4,2,5,6,0,99]
    cpu = intcode.CPU(memory=mem)
    cpu.execute()
    assert mem == becomes
