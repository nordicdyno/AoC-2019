import intcode
# from robopaint import Direction, change_direction, move_to_direction
import robopaint

if __name__ == "__main__":
    amplifiers = []
    program = intcode.read_file('code.txt')

    cpu = intcode.CPU(code=program)
    robo = robopaint.Robot(cpu=cpu)

    robo.paint(start_color=robopaint.ColorNum.White)
    robo.draw_painted()

