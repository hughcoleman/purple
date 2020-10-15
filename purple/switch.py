#!/usr/bin/env python
# -*- coding: utf-8 -*-

# switch.py
# Copyright (c) 2013 Brian Neal
# Copyright (c) 2020 Hugh Coleman
# 
# This file is part of hughcoleman/purple, a historically accurate simulator of
# the PURPLE (Type-B) Cipher Machine. It is released under the MIT License (see
# LICENSE.)

""" Implement a stepping switch.
 
Stepping switches were responsible for performing the obfuscation of sensitive 
materials. """

class SteppingSwitchError(RuntimeError):
    pass

class SteppingSwitch:

    def step(self):
        """ Step the wiper arm one position forwards. """
        self.position = (self.position + 1) % len(self.logic)

    def encrypt(self, n):
        """ Feed the value 'n' backwards through the stepping switch. """
        return self.logic[self.position].index(n)

    def decrypt(self, n):
        """ Feed the value 'n' forwards through the stepping switch. """
        return self.logic[self.position][n]
    
    def __init__(self, logic, position=0):
        """ Construct a stepping switch with the given logic. """
        self.logic = logic
        self.position = position

        if any(len(self.logic[0]) != len(self.logic[n]) for n in range(len(logic))):
            raise SteppingSwitchError("The specific logic matrix has uneven dimensions.")
    
        if (self.position < 0) or (self.position >= len(self.logic)):
            raise SteppingSwitchError("Illegal switch position.")
