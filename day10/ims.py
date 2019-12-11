"""
    IMS - Instant Monitoring Station
"""
from enum import IntEnum
from typing import List, Dict, Callable, Type, Iterable, Tuple
from dataclasses import dataclass, field
import functools
from dataclasses import dataclass, field
import math

Point = Tuple[int, int]

def normalize_points(p1: Point, p2: Point) -> Tuple[Point, Point]:
    (x1, y1) = p1
    (x2, y2) = p2
    # normailze from/to pair
    # y always grow, if y is equal x is always grow
    if (y1 > y2) or (y1 == y2 and x1 > x2):
        (x2, y2, x1, y1) = (x1, y1, x2, y2)
    return (x1, y1, x2, y2)

Vector = Tuple

def vectors_angle(v1: Vector, v2: Vector) -> float:
    a = math.degrees(math.atan2(*v1) - math.atan2(*v2))
    if a < 0:
        a = 360 + a
    return a

@dataclass
class Map():
    coords: List[List[int]]
    seen: Dict[Tuple[Point, Point], bool] = field(default_factory=lambda: {}, init=False)

    def loop_scan(self, p: Point) -> Point:
        v1 = (0, p[1])
        # print("get visible")
        visible = self.find_visible(p)
        for p in sorted(visible, key=lambda x: vectors_angle(v1, (p[0]-x[0], p[1]-x[1]))):
            yield p


    def vaporize(self, p: Point):
        # print("vaporize", p)
        self.coords[p[1]][p[0]] = 0
        self.seen = {} # invalidate cache

    def best_observer(self) -> (int, Point):
        observers = self.observerability()
        max_value, max_key = 0, (None, None)
        for k, v in observers.items():
            if v <= max_value:
                continue
            max_value = v
            max_key = k
        return (max_value, max_key)

    def find_visible(self, point: Point):
        asteroids = self.asteroids()
        found = []
        for point2 in asteroids:
            # print(f"{point1} vs {point2}")
            visible = self.check_if_visible(point, point2)
            if visible:
                found.append(point2)
        return found


    def asteroids(self) -> Dict[Point,int]:
        asteroids = {}
        for y in range(0, len(self.coords)):
            for x, value in enumerate(self.coords[y]):
                if value:
                    asteroids[(x,y)] = 0
        return asteroids

    def observerability(self) -> Dict[Point,int]:
        asteroids = self.asteroids()
        for point in asteroids:
            # for point2 in asteroids:
            #     visible = self.check_if_visible(point1, point2)
            #     if visible:
            asteroids[point] += len(self.find_visible(point))
        return asteroids

    def check_if_visible(self, p1: Point, p2: Point) -> bool:
        # print("  coords:", p1, "->", p2)
        if p1 == p2:
            # raise("coordinates the same")
            return False

        (x1, y1, x2, y2) = normalize_points(p1, p2)
        seen_key = ((x1,y1), (x2,y2))
        v = self.seen.get(seen_key)
        if v is not None:
            return v
        self.seen[seen_key] = True

        x_dist, y_dist = abs(x2-x1), abs(y2-y1)
        # print(f"y_dist: {y_dist}; x_dist: {x_dist}")

        gcd = math.gcd(x_dist, y_dist)
        x_step, y_step = int(x_dist/gcd), int(y_dist/gcd)
        # print(f"y_step: {y_step}; x_step: {x_step}")

        # y always grown
        if y_step == 0:
            y_iter = (y1 for i in range(0,x_dist))
        else:
            y_iter = range(y1+y_step, y2, y_step)

        if x_step == 0:
            x_iter = (x1 for i in range(0,y_dist))
        else:
            x_start, x_end = x1, x2
            if x_start > x_end:
                x_start, x_end = x_end, x_start
            x_iter = range(x_start+x_step, x_end, x_step)
            if x1 > x2:
                x_iter = reversed(x_iter)

        for x, y in zip(x_iter, y_iter):
            # print(f"ZIP: x={x}, y={y}; value: {self.coords[y][x]}")
            # for cY, row in enumerate(self.coords):
            #     for cX, p in enumerate(row):
            #         fmt = f" {p}"
            #         if cX == x and cY == y:
            #             fmt = f" \033[4m{p}\033[0m"
            #         print(fmt, end='')
            #     print()

            if not self.coords[y][x]:
                continue

            self.seen[normalize_points((x1, y1), (x,y))] = True
            self.seen[seen_key] = False
            return False

        return True

    def __str__(self):
        lines = []
        for cY, row in enumerate(self.coords):
            lines.append("".join([f" {p}" for p in row]))
        return "\n".join(lines)

def read_file(file: str) -> List:
    with open(file) as f:
        return parse(f)

def parse(lines: Iterable):
    coords = []
    for line in lines:
        line = line.rstrip("\n").replace(" ", "")
        if not line:
            continue
        row = [1 if x == "#" else 0 for x in line]
        coords.append(row)
    return coords
