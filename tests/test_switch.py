#!/usr/bin/env python
# -*- coding: utf-8 -*-

# test_switch.py
# Copyright (c) 2013 Brian Neal
# Copyright (c) 2020 Hugh Coleman
# 
# This file is part of hughcoleman/purple, a historically accurate simulator of
# the PURPLE (Type-B) Cipher Machine. It is released under the MIT License (see
# LICENSE.)

import unittest

from purple.switch import SteppingSwitch, SteppingSwitchError
from purple.wiring import SIXES

class TestSwitch(unittest.TestCase):

    def test_construction(self):
        bad_wiring = [
            [1, 2, 0],
            [2, 1],
            [0, 1, 2]
        ]

        good_wiring = [
            [1, 2, 0],
            [2, 1, 0],
            [0, 1, 2]
        ]

        self.assertRaises(SteppingSwitchError, SteppingSwitch, bad_wiring)
        self.assertRaises(SteppingSwitchError, SteppingSwitch, bad_wiring,
            position=0)
        self.assertRaises(SteppingSwitchError, SteppingSwitch, good_wiring,
            position=-1)
        self.assertRaises(SteppingSwitchError, SteppingSwitch, good_wiring,
            position=3)
        self.assertRaises(SteppingSwitchError, SteppingSwitch, bad_wiring,
            position=3)

    def test_step(self):
        switch = SteppingSwitch(SIXES)

        for n in range(25 * 2 + 1):
            self.assertEqual(n % 25, switch.position)
            switch.step()
            self.assertEqual((n + 1) % 25, switch.position)

    def test_decrypt(self):
        switch = SteppingSwitch(SIXES)

        self.assertEqual(switch.decrypt(0), 1)
        self.assertEqual(switch.decrypt(1), 0)
        self.assertEqual(switch.decrypt(2), 2)
        self.assertEqual(switch.decrypt(3), 4)
        self.assertEqual(switch.decrypt(4), 3)
        self.assertEqual(switch.decrypt(5), 5)
    
    def test_encrypt(self):
        switch = SteppingSwitch(SIXES)

        self.assertEqual(switch.encrypt(0), 1)
        self.assertEqual(switch.encrypt(1), 0)
        self.assertEqual(switch.encrypt(2), 2)
        self.assertEqual(switch.encrypt(3), 4)
        self.assertEqual(switch.encrypt(4), 3)
        self.assertEqual(switch.encrypt(5), 5)