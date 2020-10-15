#!/usr/bin/env python
# -*- coding: utf-8 -*-

# switch.py
# Copyright (c) 2013 - 2014 Brian Neal
# Copyright (c) 2020 Hugh Coleman
# 
# This file is part of hughcoleman/purple, a historically accurate simulator of
# the PURPLE (Type-B) Cipher Machine. It is released under the MIT License (see
# LICENSE.)

""" This implements Purple97, a historically accurate simulator of the PURPLE 
(Type-B) Cipher Machine.
"""

from purple.switch import SteppingSwitch
from purple.wiring import SIXES, TWENTIES_I, TWENTIES_II, TWENTIES_III

from collections import Counter
import string
import re

class Purple97Error(RuntimeError):
    pass

class Purple97:
    """ This class simulates the top-level behavior of the PURPLE cipher
    machine.

    """
    CHARSET = set(string.ascii_uppercase)
    PLUGBOARD = 'AEIOUYBCDFGHJKLMNPQRSTVWXZ'

    @classmethod
    def from_keysheet(self, settings, plugboard=None):
        """ This method allows one to construct a machine from the shorthand 
        notation used by American codebreakers.
        """

        shorthand = re.compile(r"\b(0?[1-9]|1[0-9]|2[0-5])\-(0?[1-9]|1[0-9]|2[0-5])\,(0?[1-9]|1[0-9]|2[0-5])\,(0?[1-9]|1[0-9]|2[0-5])\-([1-3])([1-3])\b")

        if not (groups := re.search(shorthand, settings)):
            raise Purple97Error("Unrecognized shorthand format.")
        
        return self(
            [int(groups.group(n)) - 1 for n in [1, 2, 3, 4]],
            int(groups.group(5)), int(groups.group(6)),
            plugboard
        )

    def decrypt(self, ciphertext):
        """ Decrypts the given ciphertext and returns the plaintext output. """

        plaintext = []
        for c in ciphertext:

            # skip illegible characters
            if (c in ["-", "/", " "]):
                plaintext.append(c)

            elif (c not in self.CHARSET):
                raise Purple97Error(f"invalid character \"{c}\" in ciphertext")

            else:
                n = self.plugboard[c]

                if (n < 6):
                    x = self.sixes.decrypt(n)
                else:
                    # This input goes to the chain of twenties switches
                    n -= 6
                    x = self.twenties[0].decrypt(
                            self.twenties[1].decrypt(
                                self.twenties[2].decrypt(n)
                            )
                        )
                    x += 6

                plaintext.append(self.alphabet[x])

            self.step()

        return ''.join(plaintext)

    def encrypt(self, plaintext):
        """ Encrypts the given plaintext and returns the ciphertext output. """

        ciphertext = []
        for c in plaintext:

            if (c not in self.CHARSET):
                raise Purple97Error(f"invalid character \"{c}\" in plaintext")

            n = self.plugboard[c]
            if n < 6:
                x = self.sixes.encrypt(n)
            else:
                n -= 6
                x = self.twenties[2].encrypt(
                        self.twenties[1].encrypt(
                            self.twenties[0].encrypt(n)
                        )
                    )
                x += 6

            ciphertext.append(self.alphabet[x])

            self.step()

        return ''.join(ciphertext)

    def step(self):
        """ Step the stepping switches. """
        # First read the sixes and middle switch
        # positions before stepping anything. Use these latched values in
        # the decision processes for stepping a twenties. This is crucial!
        sixes_pos = self.sixes.position
        middle_pos = self.middle_switch.position

        # Now we can step the sixes. It unconditionally steps after every
        # letter is processed.
        self.sixes.step()

        # Only 1 twenties switch steps at a time.
        #
        # Normally the fast switch advances every letter.
        #
        # However if the sixes is at the last position (24), the middle
        # switch steps instead.
        #
        # But if the sixes is at the second to last position (23) and the middle
        # switch is at the last position (24), the slow switch will step.  The
        # middle switch will step on the next letter in this case.

        if sixes_pos == 23 and middle_pos == 24:
            self.slow_switch.step()
        elif sixes_pos == 24:
            self.middle_switch.step()
        else:
            self.fast_switch.step()

    def __init__(self, switches_pos=None, fast_switch=1, middle_switch=2,
            alphabet=None):
        """Build a PURPLE (Cipher Machine 97) instance. Initial settings can be
        optionally supplied.

        switches_pos: If not None, must be a 4-element list or tuple of integer
        starting switch positions. Each position must be in the range of 0-24,
        inclusive. If None, a list of all 0's is assumed. The first element in
        the list is the starting position for the sixes switch. The second
        through fourth elements are the starting positions for the three
        twenties switches, 1 through 3.

        fast_switch: this integer parameter names which twenties switch (1-3) is
        assuming the role of the fast switch.

        middle_switch: this integer parameter names which twenties switch (1-3)
        has been designated as the middle switch.

        Passing in the same value for both the fast and medium switches will
        raise a Purple97Error exception. The slow switch is assumed to be the
        remaining twenties switch that was not named.

        alphabet: this parameter must be a 26-letter sequence that represents
        the daily alphabet setting. It describes how the typewriters are wired
        to the plugboard. The first six characters are the mapping for the sixes
        switch, and the remaining 20 are for the input wiring for the first
        stage of the twenties switches. If None is supplied, a straight through
        mapping is assumed; i.e. PLUGBOARD.

        The alphabet parameter will accept either upper or lowercase letters.
        All 26 distinct letters must be present or else a Purple97Error
        exception will be raised.

        """
        # If no switch positions are supplied, default to all 0's
        if switches_pos is None:
            switches_pos = (0, 0, 0, 0)

        # Validate switch positions
        try:
            n = len(switches_pos)
        except TypeError:
            raise Purple97Error("switches_pos must be a sequence")
        if n != 4:
            raise Purple97Error("switches_pos must have length of 4")

        # Create switches with correct starting positions
        self.sixes = SteppingSwitch(SIXES, switches_pos[0])
        self.twenties = [
            SteppingSwitch(TWENTIES_I, switches_pos[1]),
            SteppingSwitch(TWENTIES_II, switches_pos[2]),
            SteppingSwitch(TWENTIES_III, switches_pos[3]),
        ]

        # Validate fast & middle switch parameters
        if not (1 <= fast_switch <= 3):
            raise Purple97Error("fast_switch out of range (1-3)")
        if not (1 <= middle_switch <= 3):
            raise Purple97Error("middle_switch out of range (1-3)")
        if fast_switch == middle_switch:
            raise Purple97Error("fast & middle switches cannot be the same")

        # Store references to the fast, middle, and slow switches
        self.fast_switch = self.twenties[fast_switch - 1]
        self.middle_switch = self.twenties[middle_switch - 1]

        # Pick the remaining switch as the slow switch
        switches = [1, 2, 3]
        switches.remove(fast_switch)
        switches.remove(middle_switch)
        self.slow_switch = self.twenties[switches[0] - 1]

        # Validate the alphabet
        if alphabet is None:
            alphabet = self.PLUGBOARD

        if len(alphabet) != 26:
            raise Purple97Error("invalid alphabet length")
        alphabet = alphabet.upper()

        if set(alphabet) != self.CHARSET:
            raise Purple97Error("invalid alphabet")

        self.alphabet = alphabet
        self.plugboard = {c : n for n, c in enumerate(alphabet)}
