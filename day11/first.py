import intcode
import robopaint
# from robopaint import Direction, change_direction, move_to_direction

print("probe program")


# def probe_paint_code(cpu: intcode.CPU):
#     # cpu.debug = True
#     cpu.max_steps = 100_000

#     painted_once = 0
#     paints_count = 0
#     painted = {}
#     default_color = 0
#     cpu.set_input([default_color])

#     x, y = 0, 0
#     direction = Direction.Up
#     while True:
#         try:
#             while cpu.next_op():
#                 # print(cpu.state())
#                 pass
#         except intcode.OutputInt:
#             # print("==CURRENT OUTPUT:", cpu.output)
#             last_out = cpu.output[-1]
#             if len(cpu.output) % 2 == 1:
#                 p = (x,y)
#                 if painted.get(p, None) is None:
#                     # print(p)
#                     painted_once += 1
#                 paints_count += 1
#                 painted[p] = last_out
#                 # print(f"==SET COLOR: of ({p}) to {last_out}")
#             else:
#                 # print(f"==CHANGE_DIRECTION: {last_out} from {direction}")
#                 direction = change_direction(direction, last_out)
#                 # print(f"==MOVE_TO_DIRECTION: {direction} from ({x},{y})", end='')
#                 x, y = move_to_direction(direction, (x, y))
#                 # print(f" to ({x},{y})")
#                 color = painted.get((x,y), default_color)
#                 # print(f"==SET INPUT: {color}")
#                 cpu.set_input([color])
#             continue
#         except intcode.HaltInt:
#             print("STOP: Got HaltInt")
#             print("")
#             print("CPU STATE:")
#             print(cpu.state())
#             pass
#         break
#     print("painted_once =", painted_once)
#     print("paints_count =", paints_count)
#     print("len(painted) =", len(painted))

# if __name__ == "__main__":
#     amplifiers = []
#     program = intcode.read_file('code.txt')
#     cpu = intcode.CPU(code=program, input=[1])
#     probe_paint_code(cpu)

if __name__ == "__main__":
    amplifiers = []
    program = intcode.read_file('code.txt')

    cpu = intcode.CPU(code=program)
    robo = robopaint.Robot(cpu=cpu)

    robo.paint(start_color=robopaint.ColorNum.Black)
    robo.draw_painted()

    print(robo.painted_count())