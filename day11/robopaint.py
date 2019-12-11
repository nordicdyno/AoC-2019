from dataclasses import dataclass, field
from enum import Enum, IntEnum
import intcode
from typing import List, Dict, Callable, Type, Tuple, Any


Point = Tuple[int, int]

class ColorNum(IntEnum):
    Black = 0 # 0 for robot
    White = 1 # 1 for robot

class Color(Enum):
    Black = '.' # 0 for robot
    White = '#' # 1 for robot

class Rotate(IntEnum):
    Left = 0
    Right = 1

class Direction(Enum):
    Left = '<'
    Right = '>'
    Up = '^'
    Down = 'v'

directionRelations = {
    Direction.Left: [Direction.Down, Direction.Up],
    Direction.Right: [Direction.Up, Direction.Down],
    Direction.Up: [Direction.Left, Direction.Right],
    Direction.Down: [Direction.Right, Direction.Left],
}
def change_direction(direction: Direction, turn: int) -> Direction:
    return directionRelations[direction][turn]

directionMove = {
    Direction.Left: (-1, 0),
    Direction.Right:( 1, 0),
    Direction.Up:   ( 0,-1),
    Direction.Down: ( 0, 1),
}
def move_to_direction(direction: Direction, p: Point) -> Point:
    x, y = directionMove[direction]
    return  p[0]+x, p[1]+y

@dataclass
class Robot():
    cpu: intcode.CPU
    painted: Dict[Any, Any] = field(default_factory=lambda: {})
    painted_once: int = 0

    def painted_count(self) -> int:
        return len(self.painted)

    def draw_painted(self):
        min_x, min_y, max_x, max_y = 0, 0, 0, 0
        for (x,y) in self.painted:
            if x < min_x:
                min_x = x
            if x > max_x:
                max_x = x
            if y < min_y:
                min_y = y
            if y > max_y:
                max_y = y
        # print(self.painted)
        # print(f"DIMENSIONS: {min_x}, {min_y} -> {max_x}, {max_y}")

        # print("Y:", 0, max_y-min_y+1)
        # print("X:", 0, max_x-min_x+1)

        for y in range (0, max_y-min_y+1):
            for x in range (0, max_x-min_x+1):
                p = ((min_x+x), (min_y+y))
                # print(p)
                color = self.painted.get(p, ColorNum.Black)
                if color == 0:
                    color = "  "
                else:
                    color = " #"
                print(f"{color}", end='')
            print()

    def paint(self, start_color: ColorNum=ColorNum.Black):
        cpu = self.cpu
        x, y = 0, 0
        self.painted[(x,y)] = start_color # start with provided color
        cpu.set_input([start_color]) #

        direction = Direction.Up
        while True:
            try:
                while cpu.next_op():
                    pass
            except intcode.OutputInt:
                last_out = cpu.output[-1]
                if len(cpu.output) % 2 == 1:
                    p = (x,y)
                    # if painted.get(p, None) is None:
                    #     painted_once += 1
                    # paints_count += 1
                    self.painted[p] = last_out
                    # print(f"==SET COLOR: of ({p}) to {last_out}")
                else:
                    direction = change_direction(direction, last_out)
                    # print(f" ==NEW DIRECTION: {direction}")
                    x, y = move_to_direction(direction, (x, y))
                    color = self.painted.get((x,y), ColorNum.Black)
                    cpu.set_input([color])
                continue
            except intcode.HaltInt:
                print("STOP: Got HaltInt")
                print("")
                print("CPU STATE:")
                print(cpu.state())
                pass
            break