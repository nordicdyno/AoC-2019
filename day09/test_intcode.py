import intcode

def test_memory_rw():
    cpu = intcode.CPU(code=[])
    value = 1125899906842624
    cpu.write_memory(10000, value)
    got_value = cpu.read_memory(10000)
    assert value == got_value

def test_parse_opcode():
    got_op, got_modes = intcode.parse_instruction(109)
    assert 9 == got_op
    assert [1,0,0,0,0] == got_modes

    got_op, got_modes = intcode.parse_instruction(9)
    assert 9 == got_op
    assert [0,0,0,0,0] == got_modes

    got_op, got_modes = intcode.parse_instruction(1102)
    assert 2 == got_op
    assert [1,1,0,0,0] == got_modes
    # assert mem == becomes

    got_op, got_modes = intcode.parse_instruction(204)
    assert 4 == got_op
    assert [2,0,0,0,0] == got_modes

def test_case1():
    prog = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
    cpu = intcode.CPU(code=prog)
    # print()
    # cpu.debug = True
    cpu.execute()
    assert cpu.output == prog

def test_case2():
    prog = [
        1102,34915192,34915192,7, # write 1219070632396864 to [7] (last elem)
        4,7, # re
        99,0
    ]
    cpu = intcode.CPU(code=prog)
    # print("")
    # cpu.debug = True
    cpu.execute()
    assert 16 == len(str(cpu.last_output()))

def test_case3():
    prog = [104,1125899906842624,99]
    cpu = intcode.CPU(code=prog)
    # print("")
    # cpu.debug = True
    cpu.execute()
    # print("case3 output:", cpu.output)
    assert [1125899906842624] == cpu.output
