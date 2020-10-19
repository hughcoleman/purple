#!/usr/bin/env python
# -*- coding: utf-8 -*-

# switch.py
# Copyright (c) 2013 - 2014 Brian Neal
# Copyright (c) 2020 Hugh Coleman
# 
# This file is part of hughcoleman/system97, a historically accurate simulator 
# of the "System 97" or Type-B Cipher Machine. It is released under the MIT 
# License (see LICENSE.)

""" This implements System97, a historically accurate simulator of the 
"System 97" or Type-B Cipher Machine.
"""

import system97.switch
import system97.logic

import string

class System97:
    """ This class implements a historically accurate simulator of the 
    "System 97" or Type-B Cipher Machine.

    """

    CHARSET = set(string.ascii_uppercase)

    def decrypt(self, ciphertext):
        """ Decrypts the given ciphertext and returns the plaintext output. """

        plaintext = []
        for c in ciphertext:

            if (c in ["-", "/", " "]):
                plaintext.append(c)
                self.step()
                continue

            n = self.plugboard.index(c)
            if (n < 6):
                x = self.sixes.decrypt(n)
            else:
                x = self.twenties[1].decrypt(
                        self.twenties[2].decrypt(
                            self.twenties[3].decrypt(n)
                        )
                    )

            plaintext.append(self.plugboard[x])
            self.step()

        return ''.join(plaintext)

    def encrypt(self, plaintext):
        """ Encrypts the given plaintext and returns the ciphertext output. """

        ciphertext = []
        for c in plaintext:

            if (c in ["-", "/", " "]):
                ciphertext.append(c)
                self.step()
                continue

            n = self.plugboard.index(c)
            if n < 6:
                x = self.sixes.encrypt(n)
            else:
                x = self.twenties[3].encrypt(
                        self.twenties[2].encrypt(
                            self.twenties[1].encrypt(n)
                        )
                    )

            ciphertext.append(self.plugboard[x])
            self.step()

        return ''.join(ciphertext)

    def step(self):
        """ Step the stepping switches.
        
        After every character, only one of the three twenties switches steps.
        The switch that steps is determined by the following rules.

         - If the sixes switch is at the second-to-last position (23) and the
           medium-speed switch is at the last position (24), the slow-speed
           switch will step.
         - If the sixes switch is at the last position (24), the middle-speed
           switch steps.
         - In all other cases, the fast-speed switch steps.
        
        The sixes switch always steps.
        """

        if (self.sixes.position == 23) and (self.medium.position == 24):
            self.slow.step()
        elif (self.sixes.position == 24):
            self.medium.step()
        else:
            self.fast.step()

        self.sixes.step()

    def __init__(self, positions={6: 0, 20: (0, 0, 0)},\
                       speeds=(1, 2, 3),
                       plugboard="AEIOUYBCDFGHJKLMNPQRSTVWXZ"):

        # initialize switches with the supplied starting positions
        self.sixes = system97.switch.SteppingSwitch(
            system97.logic.SIXES, positions[6]
        )
        self.twenties = [
            None, # so that the twenties are each indexed into the list by 
                  # their numerical value
            system97.switch.SteppingSwitch(
                system97.logic.TWENTIES_I, positions[20][0]
            ),
            system97.switch.SteppingSwitch(
                system97.logic.TWENTIES_II, positions[20][1]
            ),
            system97.switch.SteppingSwitch(
                system97.logic.TWENTIES_III, positions[20][2]
            )
        ]

        # store references to the fast, middle, and slow switches
        self.fast = self.twenties[speeds[0]]
        self.medium = self.twenties[speeds[1]]
        self.slow = self.twenties[speeds[2]]

        self.plugboard = plugboard