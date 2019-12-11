from sif import *
from typing import List, Dict, Callable, Type


def test_decode_layers():
    sif = split_digits("123456789012")
    layers = decode_layers(sif, 3, 2)
    img1 = [[1,2,3], [4,5,6]]
    img2 = [[7,8,9],[0,1,2]]
    expect = [img1, img2]
    assert 2 == len(layers)
    assert expect == layers

def find_fewest_layer_idx(layers: List, elem: int) -> int:
    min_n, min_count = 0, None
    for n, img in enumerate(layers):
        elem_count = count_layer_digits(img, elem)
        if (min_count is not None) and (elem_count >= min_count):
            continue
        min_n, min_count = n, elem_count
    return min_n

def count_layer_digits(img: List[int], elem: int) -> int:
    return [x for x in chain(*img)].count(elem)

def test_find_fewest():
    sif = split_digits("103456" + "789212" + "780012")
    layers = decode_layers(sif, 3, 2)
    n = find_fewest_layer_idx(layers, 0)
    assert 1 == n

def test_find_first():
    img_input = read_file("input.txt")
    layers = decode_layers(img_input, 25, 6)
    n = find_fewest_layer_idx(layers, 0)
    result = count_layer_digits(layers[n], 1) * count_layer_digits(layers[n], 2)
    assert 1935 == result

def test_merge_layers():
    sif = split_digits("0222", "1122", "2212", "0000")
    # print("sif:", sif)
    layers = decode_layers(sif, 2, 2)
    merged = merge_layers(layers)
    # print("merged:", merged)
    assert [[0, 1], [1, 0]] == merged

def test_second():
    img_input = read_file("input.txt")
    layers = decode_layers(img_input, 25, 6)
    merged = merge_layers(layers)
    result = image2ascii(merged)
    expect_CFLUL = """
  1 1     1 1 1 1   1         1     1   1         
1     1   1         1         1     1   1         
1         1 1 1     1         1     1   1         
1         1         1         1     1   1         
1     1   1         1         1     1   1         
  1 1     1         1 1 1 1     1 1     1 1 1 1   
"""
    expect_CFLUL = expect_CFLUL[expect_CFLUL.index("\n")+1:].rstrip("\n")
    assert expect_CFLUL == result
