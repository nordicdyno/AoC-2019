"""
    SIF - Space Image Format
    https://adventofcode.com/2019/day/8
"""
from typing import List, Dict, Callable, Type
from dataclasses import dataclass, field
from itertools import chain

def split_digits(*args) -> List[int]:
    return [int(x) for x in chain(*args)]

def read_file(sif_file: str) -> List:
    codes = []
    with open(sif_file) as f:
        for line in f:
            if not line:
                continue
            codes.extend(split_digits(line))
    return codes


def decode_layers(encode: List[int], width: int, height: int):
    result = []
    size = width*height
    for img_idx in range(0, len(encode), size):
        img = []
        for row_idx in range(0, size, width):
            img.append(encode[img_idx+row_idx:img_idx+row_idx+width])
        result.append(img)
    return result

Transparent = 2

def merge_layers(layers: List):
    output = None
    w, h = None, None
    for layer in layers:
        if output is None:
            output = list(chain(*layer))
            w = len(layer[0])
            h = len(layer)
            continue
        for i, code in enumerate(chain(*layer)):
            if output[i] == Transparent:
                output[i] = code
    return decode_layers(output, w, h)[0]

def image2ascii(img: List[List[int]]):
    lines = []
    for row in img:
        lines.append("".join([f"{code if code != 0 else ' '} " for code in row]))
    return "\n".join(lines)
