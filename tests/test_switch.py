#!/usr/bin/env python
# -*- coding: utf-8 -*-

# test_switch.py
# Copyright (c) 2013 Brian Neal
# Copyright (c) 2020 Hugh Coleman
# 
# This file is part of hughcoleman/system97, a historically accurate simulator 
# of the "System 97" or Type-B Cipher Machine. It is released under the MIT 
# License (see LICENSE.)

import unittest

import system97.switch
import system97.logic

class TestSwitch(unittest.TestCase):

    def test__illegal_routing_logic(self):
        """ Ensure that SteppingSwitch.__init__ raises a ValueError if an
        incorrectly-balanced routing matrix is supplied.
        """

        illegal_routing_logic = {
            0: [0, 1, 2],
            1: [2, 1],
            2: [1, 1, 2]
        }

        self.assertRaises(ValueError, system97.switch.SteppingSwitch, {
            "routing_logic": illegal_routing_logic,
            "position": 0,
            "size": 3
        })

    def test__illegal_arm_position(self):
        """ Ensure that SteppingSwitch.__init__ raises a ValueError if an
        illegal initial arm position is supplied.
        """

        illegal_positions = [
            -1,
            25,
            99
        ]

        for position in illegal_positions:
            self.assertRaises(ValueError, system97.switch.SteppingSwitch, {
                "routing_logic": {},
                "position": position
            })

    def test__step(self):
        """ Ensure that SteppingSwitch.step correctly tracks the position of 
        the arm.
        """
        switch = system97.switch.SteppingSwitch(system97.logic.SIXES)

        for position in range(25*2 + 1):
            self.assertEqual(position % 25, switch.position)
            switch.step()
    
    def test__encrypt(self):
        """ Ensure that SteppingSwitch.encrypt properly routes the supplied
        signal.
        """

        switch = system97.switch.SteppingSwitch(system97.logic.SIXES)

        for position in range(25):
            for pt in range(6):
                self.assertEqual(
                    system97.logic.SIXES[switch.encrypt(pt)][position],
                    pt
                )
            
            switch.step()

    def test__decrypt(self):
        """ Ensure that SteppingSwitch.decrypt properly routes the supplied
        signal.
        """

        switch = system97.switch.SteppingSwitch(system97.logic.SIXES)

        for position in range(25):
            for ct in range(6):
                self.assertEqual(
                    system97.logic.SIXES[ct][position],
                    switch.decrypt(ct)
                )
            
            switch.step()
