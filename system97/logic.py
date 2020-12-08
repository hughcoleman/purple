#!/usr/bin/env python
# -*- coding: utf-8 -*-

# logic.py
# Copyright (c) 2013 Brian Neal
# Copyright (c) 2020 Hugh Coleman
#
# This file is part of hughcoleman/system97, a historically accurate simulator
# of the "System 97" or Type-B Cipher Machine. It is released under the MIT
# License (see LICENSE.)

""" This file encodes the wiring logic of the four stepping switches used in
the Type-B cipher machine. This information was extracted from the following
publication.

    Freeman, W., Sullivan, G., & Weierud, F. (2003). "Purple Revealed:
        Simulation And Computer-Aided Cryptanalysis Of Angooki Taipu B."
        Cryptologia, 27(1), 1–43. https://doi.org/10.1080/0161-110391891739

Each stepper switch's wiring logic is encoded in a two-dimensional array. The
rows are each associated with an input letter, and the columns are each
associated with a wiper arm position.
"""

SIXES = {
    0: [1, 5, 0, 3, 2, 1, 5, 2, 4, 3, 1, 4, 2, 3, 0, 4, 5, 1, 0, 2, 5, 0, 5, 3, 4],
    1: [0, 2, 4, 2, 5, 0, 4, 5, 3, 4, 0, 3, 0, 1, 5, 3, 1, 2, 1, 0, 4, 2, 3, 5, 1],
    2: [2, 4, 3, 1, 0, 5, 3, 0, 1, 2, 3, 5, 1, 4, 1, 2, 4, 3, 2, 5, 0, 5, 4, 0, 3],
    3: [4, 1, 5, 0, 3, 4, 1, 3, 5, 1, 4, 2, 5, 0, 2, 5, 2, 0, 4, 3, 1, 3, 0, 1, 2],
    4: [3, 0, 1, 5, 4, 2, 0, 4, 2, 0, 5, 1, 3, 2, 4, 0, 3, 4, 5, 1, 3, 1, 2, 4, 5],
    5: [5, 3, 2, 4, 1, 3, 2, 1, 0, 5, 2, 0, 4, 5, 3, 1, 0, 5, 3, 4, 2, 4, 1, 2, 0],
}

TWENTIES_I = {
    6: [
        11,
        9,
        22,
        8,
        24,
        7,
        21,
        6,
        22,
        17,
        25,
        10,
        20,
        16,
        17,
        13,
        12,
        15,
        18,
        6,
        14,
        23,
        21,
        10,
        19,
    ],
    7: [
        24,
        10,
        6,
        19,
        11,
        16,
        12,
        25,
        14,
        13,
        6,
        9,
        22,
        17,
        21,
        20,
        8,
        18,
        12,
        7,
        25,
        20,
        23,
        13,
        15,
    ],
    8: [
        19,
        21,
        18,
        25,
        13,
        14,
        11,
        12,
        16,
        22,
        21,
        20,
        15,
        12,
        7,
        23,
        10,
        9,
        14,
        8,
        17,
        7,
        24,
        6,
        9,
    ],
    9: [
        6,
        22,
        11,
        9,
        25,
        19,
        23,
        21,
        13,
        14,
        16,
        7,
        24,
        8,
        12,
        6,
        23,
        19,
        17,
        9,
        10,
        18,
        15,
        20,
        13,
    ],
    10: [
        15,
        19,
        20,
        11,
        18,
        12,
        14,
        17,
        25,
        8,
        7,
        18,
        21,
        13,
        9,
        17,
        22,
        23,
        25,
        10,
        15,
        6,
        16,
        24,
        14,
    ],
    11: [
        9,
        6,
        16,
        21,
        10,
        24,
        15,
        19,
        23,
        25,
        22,
        24,
        7,
        20,
        13,
        16,
        18,
        8,
        21,
        11,
        22,
        12,
        25,
        14,
        17,
    ],
    12: [
        7,
        25,
        24,
        13,
        23,
        11,
        18,
        10,
        12,
        9,
        14,
        11,
        16,
        21,
        20,
        22,
        24,
        7,
        19,
        12,
        6,
        15,
        10,
        17,
        8,
    ],
    13: [
        12,
        20,
        17,
        24,
        9,
        8,
        6,
        23,
        19,
        15,
        9,
        21,
        13,
        11,
        24,
        19,
        25,
        22,
        15,
        13,
        18,
        10,
        14,
        7,
        16,
    ],
    14: [
        18,
        8,
        21,
        7,
        15,
        23,
        22,
        20,
        6,
        19,
        13,
        17,
        14,
        9,
        10,
        25,
        19,
        16,
        24,
        14,
        12,
        24,
        6,
        11,
        22,
    ],
    15: [
        14,
        13,
        23,
        17,
        8,
        18,
        7,
        15,
        21,
        10,
        20,
        19,
        12,
        25,
        6,
        21,
        16,
        24,
        11,
        15,
        20,
        22,
        9,
        8,
        25,
    ],
    16: [
        13,
        23,
        15,
        22,
        21,
        17,
        10,
        18,
        20,
        12,
        15,
        13,
        8,
        7,
        16,
        18,
        14,
        25,
        6,
        16,
        9,
        11,
        17,
        19,
        24,
    ],
    17: [
        21,
        16,
        8,
        14,
        20,
        13,
        9,
        11,
        10,
        23,
        18,
        12,
        19,
        10,
        14,
        24,
        15,
        6,
        7,
        17,
        8,
        25,
        18,
        22,
        11,
    ],
    18: [
        8,
        17,
        12,
        10,
        19,
        15,
        16,
        13,
        24,
        7,
        8,
        22,
        23,
        6,
        25,
        14,
        7,
        11,
        16,
        18,
        21,
        14,
        12,
        9,
        20,
    ],
    19: [
        23,
        18,
        19,
        6,
        17,
        20,
        24,
        8,
        7,
        21,
        23,
        15,
        18,
        14,
        22,
        12,
        11,
        17,
        9,
        19,
        13,
        16,
        11,
        25,
        10,
    ],
    20: [
        20,
        15,
        13,
        16,
        12,
        21,
        25,
        9,
        11,
        18,
        19,
        23,
        17,
        24,
        11,
        8,
        6,
        14,
        10,
        20,
        23,
        17,
        22,
        21,
        7,
    ],
    21: [
        16,
        24,
        25,
        15,
        7,
        22,
        19,
        14,
        17,
        11,
        10,
        8,
        6,
        23,
        19,
        9,
        20,
        12,
        8,
        21,
        16,
        13,
        7,
        18,
        23,
    ],
    22: [
        10,
        7,
        9,
        12,
        22,
        25,
        13,
        16,
        9,
        6,
        11,
        14,
        10,
        15,
        18,
        7,
        17,
        20,
        23,
        22,
        24,
        8,
        19,
        23,
        21,
    ],
    23: [
        17,
        11,
        14,
        18,
        16,
        9,
        20,
        22,
        15,
        24,
        12,
        6,
        25,
        19,
        8,
        10,
        21,
        13,
        22,
        23,
        7,
        9,
        20,
        15,
        12,
    ],
    24: [
        25,
        14,
        7,
        20,
        6,
        10,
        8,
        24,
        18,
        20,
        17,
        16,
        11,
        22,
        23,
        15,
        9,
        10,
        13,
        24,
        19,
        21,
        8,
        12,
        6,
    ],
    25: [
        22,
        12,
        10,
        23,
        14,
        6,
        17,
        7,
        8,
        16,
        24,
        25,
        9,
        18,
        15,
        11,
        13,
        21,
        20,
        25,
        11,
        19,
        13,
        16,
        18,
    ],
}

TWENTIES_II = {
    6: [
        20,
        17,
        9,
        11,
        12,
        10,
        13,
        25,
        14,
        15,
        16,
        7,
        21,
        24,
        23,
        25,
        8,
        10,
        19,
        13,
        22,
        6,
        21,
        24,
        18,
    ],
    7: [
        14,
        11,
        23,
        16,
        7,
        22,
        9,
        6,
        13,
        17,
        12,
        8,
        15,
        21,
        19,
        8,
        11,
        20,
        25,
        16,
        24,
        10,
        13,
        18,
        6,
    ],
    8: [
        6,
        20,
        10,
        7,
        18,
        19,
        8,
        21,
        12,
        16,
        19,
        14,
        20,
        23,
        17,
        24,
        9,
        25,
        18,
        6,
        11,
        17,
        15,
        13,
        22,
    ],
    9: [
        10,
        7,
        13,
        25,
        8,
        12,
        16,
        15,
        20,
        23,
        9,
        15,
        6,
        17,
        24,
        7,
        19,
        14,
        22,
        11,
        6,
        25,
        18,
        21,
        20,
    ],
    10: [
        22,
        9,
        21,
        19,
        14,
        15,
        24,
        20,
        10,
        13,
        23,
        18,
        22,
        8,
        6,
        9,
        7,
        15,
        10,
        24,
        17,
        11,
        16,
        25,
        12,
    ],
    11: [
        24,
        14,
        6,
        12,
        9,
        14,
        18,
        13,
        7,
        21,
        25,
        19,
        8,
        18,
        12,
        10,
        17,
        22,
        23,
        19,
        20,
        16,
        11,
        15,
        9,
    ],
    12: [
        8,
        13,
        17,
        23,
        22,
        24,
        7,
        19,
        9,
        25,
        11,
        20,
        18,
        14,
        15,
        16,
        21,
        6,
        13,
        10,
        25,
        19,
        24,
        12,
        21,
    ],
    13: [
        7,
        21,
        20,
        17,
        19,
        25,
        14,
        16,
        18,
        22,
        6,
        21,
        14,
        15,
        11,
        19,
        10,
        24,
        9,
        23,
        12,
        13,
        10,
        6,
        8,
    ],
    14: [
        15,
        24,
        25,
        20,
        6,
        13,
        17,
        23,
        22,
        10,
        18,
        12,
        9,
        11,
        16,
        14,
        23,
        18,
        7,
        22,
        21,
        14,
        8,
        7,
        19,
    ],
    15: [
        13,
        22,
        19,
        8,
        17,
        18,
        21,
        10,
        6,
        11,
        24,
        16,
        12,
        7,
        20,
        15,
        25,
        17,
        20,
        8,
        14,
        12,
        9,
        23,
        10,
    ],
    16: [
        16,
        10,
        18,
        13,
        23,
        6,
        15,
        8,
        16,
        14,
        17,
        25,
        11,
        22,
        10,
        23,
        12,
        9,
        21,
        15,
        8,
        24,
        20,
        19,
        7,
    ],
    17: [
        23,
        16,
        22,
        10,
        25,
        7,
        22,
        12,
        11,
        8,
        20,
        17,
        13,
        19,
        14,
        21,
        24,
        7,
        6,
        18,
        16,
        9,
        25,
        11,
        15,
    ],
    18: [
        17,
        25,
        16,
        15,
        11,
        21,
        19,
        18,
        24,
        9,
        10,
        23,
        7,
        16,
        13,
        20,
        6,
        12,
        14,
        17,
        18,
        8,
        22,
        14,
        23,
    ],
    19: [
        21,
        12,
        7,
        6,
        16,
        8,
        20,
        22,
        23,
        24,
        14,
        11,
        19,
        9,
        25,
        17,
        20,
        11,
        24,
        25,
        15,
        18,
        7,
        10,
        13,
    ],
    20: [
        11,
        15,
        12,
        22,
        21,
        9,
        25,
        24,
        19,
        18,
        21,
        6,
        10,
        12,
        22,
        13,
        14,
        16,
        8,
        20,
        7,
        15,
        23,
        17,
        16,
    ],
    21: [
        18,
        23,
        14,
        24,
        20,
        17,
        11,
        9,
        15,
        12,
        7,
        10,
        16,
        25,
        9,
        12,
        13,
        19,
        11,
        21,
        23,
        22,
        6,
        8,
        14,
    ],
    22: [
        25,
        6,
        11,
        14,
        10,
        16,
        23,
        7,
        8,
        6,
        22,
        13,
        17,
        20,
        8,
        18,
        15,
        21,
        12,
        9,
        13,
        23,
        19,
        22,
        24,
    ],
    23: [
        9,
        19,
        8,
        21,
        13,
        23,
        6,
        14,
        25,
        19,
        15,
        22,
        24,
        10,
        18,
        11,
        16,
        13,
        15,
        7,
        9,
        21,
        12,
        20,
        17,
    ],
    24: [
        19,
        18,
        15,
        9,
        24,
        11,
        12,
        17,
        21,
        20,
        13,
        24,
        23,
        6,
        7,
        22,
        18,
        8,
        17,
        12,
        10,
        20,
        14,
        16,
        25,
    ],
    25: [
        12,
        8,
        24,
        18,
        15,
        20,
        10,
        11,
        17,
        7,
        8,
        9,
        25,
        13,
        21,
        6,
        22,
        23,
        16,
        14,
        19,
        7,
        17,
        9,
        11,
    ],
}

TWENTIES_III = {
    6: [
        12,
        20,
        7,
        21,
        17,
        18,
        9,
        14,
        10,
        16,
        24,
        6,
        8,
        14,
        13,
        23,
        19,
        22,
        15,
        25,
        16,
        21,
        11,
        13,
        18,
    ],
    7: [
        24,
        22,
        16,
        8,
        23,
        14,
        12,
        11,
        19,
        21,
        13,
        17,
        9,
        16,
        18,
        21,
        6,
        24,
        20,
        14,
        25,
        10,
        15,
        12,
        7,
    ],
    8: [
        16,
        19,
        25,
        17,
        21,
        10,
        7,
        9,
        23,
        14,
        8,
        22,
        15,
        11,
        19,
        20,
        12,
        6,
        7,
        13,
        18,
        15,
        24,
        10,
        22,
    ],
    9: [
        8,
        7,
        17,
        14,
        9,
        11,
        20,
        15,
        22,
        23,
        20,
        18,
        17,
        10,
        21,
        9,
        25,
        16,
        19,
        11,
        13,
        24,
        21,
        6,
        12,
    ],
    10: [
        25,
        17,
        6,
        9,
        14,
        13,
        22,
        23,
        18,
        8,
        19,
        14,
        6,
        15,
        24,
        7,
        11,
        12,
        16,
        17,
        21,
        9,
        10,
        20,
        19,
    ],
    11: [
        6,
        18,
        24,
        25,
        8,
        12,
        15,
        21,
        20,
        17,
        10,
        12,
        23,
        9,
        17,
        22,
        18,
        7,
        11,
        16,
        15,
        23,
        14,
        19,
        13,
    ],
    12: [
        15,
        13,
        9,
        11,
        20,
        17,
        24,
        13,
        16,
        10,
        6,
        19,
        7,
        22,
        25,
        18,
        21,
        23,
        12,
        7,
        23,
        20,
        6,
        14,
        8,
    ],
    13: [
        11,
        8,
        15,
        24,
        18,
        22,
        10,
        19,
        17,
        20,
        16,
        7,
        13,
        24,
        12,
        17,
        23,
        9,
        6,
        10,
        19,
        22,
        25,
        21,
        14,
    ],
    14: [
        21,
        6,
        14,
        23,
        11,
        19,
        13,
        10,
        12,
        15,
        7,
        20,
        19,
        18,
        15,
        11,
        17,
        8,
        21,
        9,
        24,
        6,
        22,
        16,
        25,
    ],
    15: [
        17,
        24,
        19,
        7,
        25,
        23,
        21,
        17,
        13,
        6,
        15,
        9,
        18,
        20,
        8,
        16,
        14,
        13,
        25,
        12,
        11,
        8,
        9,
        22,
        10,
    ],
    16: [
        22,
        14,
        11,
        10,
        13,
        25,
        6,
        22,
        8,
        19,
        17,
        10,
        24,
        12,
        20,
        25,
        9,
        15,
        18,
        21,
        20,
        7,
        16,
        23,
        21,
    ],
    17: [
        18,
        9,
        20,
        13,
        7,
        15,
        17,
        6,
        11,
        22,
        21,
        16,
        12,
        7,
        14,
        24,
        22,
        10,
        8,
        19,
        9,
        25,
        23,
        11,
        15,
    ],
    18: [
        13,
        15,
        18,
        19,
        12,
        7,
        8,
        25,
        6,
        7,
        23,
        11,
        21,
        17,
        9,
        19,
        10,
        20,
        14,
        22,
        6,
        16,
        12,
        24,
        11,
    ],
    19: [
        14,
        12,
        8,
        16,
        15,
        24,
        18,
        20,
        7,
        9,
        25,
        21,
        11,
        23,
        22,
        10,
        16,
        17,
        13,
        8,
        22,
        11,
        19,
        25,
        6,
    ],
    20: [
        9,
        16,
        12,
        15,
        10,
        16,
        11,
        18,
        25,
        24,
        22,
        8,
        20,
        19,
        6,
        14,
        7,
        21,
        23,
        20,
        12,
        13,
        18,
        8,
        17,
    ],
    21: [
        23,
        25,
        21,
        6,
        24,
        20,
        19,
        24,
        9,
        11,
        12,
        13,
        14,
        25,
        16,
        6,
        8,
        14,
        22,
        15,
        10,
        18,
        7,
        17,
        20,
    ],
    22: [
        10,
        21,
        23,
        20,
        19,
        9,
        25,
        7,
        14,
        13,
        18,
        23,
        22,
        6,
        10,
        13,
        15,
        11,
        24,
        18,
        8,
        12,
        17,
        9,
        16,
    ],
    23: [
        19,
        11,
        13,
        22,
        6,
        8,
        14,
        16,
        15,
        12,
        9,
        24,
        25,
        21,
        7,
        12,
        20,
        18,
        10,
        24,
        14,
        17,
        13,
        7,
        23,
    ],
    24: [
        20,
        23,
        10,
        18,
        22,
        6,
        16,
        12,
        21,
        18,
        14,
        25,
        10,
        13,
        11,
        8,
        24,
        25,
        17,
        23,
        7,
        19,
        8,
        15,
        9,
    ],
    25: [
        7,
        10,
        22,
        12,
        16,
        21,
        23,
        8,
        24,
        25,
        11,
        15,
        16,
        8,
        23,
        15,
        13,
        19,
        9,
        6,
        17,
        14,
        20,
        18,
        24,
    ],
}
