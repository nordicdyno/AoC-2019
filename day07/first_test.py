import intcode
import first

def test_cpu_init():
    cpu = intcode.CPU(memory=[], input=[])
    assert [] == cpu.output

def test_case1():
    program = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
    phase_settings = [4,3,2,1,0]
    thruster_signal = first.check_phase_settings(program, phase_settings)
    assert 43210 == thruster_signal

def test_case2():
    program = [3,23,3,24,1002,24,10,24,1002,23,-1,23, 101,5,23,23,1,24,23,23,4,23,99,0,0]
    phase_settings = [0,1,2,3,4]
    thruster_signal = first.check_phase_settings(program, phase_settings)
    assert 54321 == thruster_signal

def test_case3():
    program = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33, 1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]
    phase_settings = [1,0,4,3,2]
    thruster_signal = first.check_phase_settings(program, phase_settings)
    assert 65210 == thruster_signal
