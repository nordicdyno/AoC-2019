from . import first

def test_add():
    mem    = [1,9,10,3,  2,3,11,0, 99,30,40,50]
    expect = [1,9,10,30+40, 2,3,11,0, 99,30,40,50]
    first.add(0, mem)
    assert mem == expect

def test_mul():
    mem    = [1,9,10,3,  2,3,11,0, 99,30,40,50]
    expect = [1,9,10,30*40, 2,3,11,0, 99,30,40,50]
    first.mul(0, mem)
    assert mem == expect

def test_run_sample0():
    mem    =  [1,9,10,3,  2,3,11,0, 99,30,40,50]
    expect = [3500,9,10,70, 2,3,11,0, 99,30,40,50]
    cpu = first.CPU(memory=mem)
    first.execute(cpu)
    assert cpu.memory == expect

def test_run_sample1():
    mem = [1,0,0,0,99]
    becomes = [2,0,0,0,99] # (1 + 1 = 2).
    cpu = first.CPU(memory=mem)
    first.execute(cpu)
    assert cpu.memory == becomes

def test_run_sample2():
    mem = [2,3,0,3,99]
    becomes = [2,3,0,6,99] # (3 * 2 = 6).
    cpu = first.CPU(memory=mem)
    first.execute(cpu)
    assert cpu.memory == becomes

def test_run_sample3():
    mem = [2,4,4,5,99,0]
    becomes = [2,4,4,5,99,9801] # (99 * 99 = 9801).
    cpu = first.CPU(memory=mem)
    first.execute(cpu)
    assert cpu.memory == becomes

def test_run_sample4():
    mem = [1,1,1,4,99,5,6,0,99]
    becomes = [30,1,1,4,2,5,6,0,99]
    cpu = first.CPU(memory=mem)
    first.execute(cpu)
    assert cpu.memory == becomes
