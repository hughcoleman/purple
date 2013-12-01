# Copyright (C) 2013 by Brian Neal.
# This file is part of purple, the PURPLE (Cipher Machine 97) simulation.
# purple is released under the MIT License (see LICENSE.txt).

"""This module contains the Purple97 class, the top level class in the PURPLE
simulation.

"""
from collections import Counter
import string

import purple.switch as switch


class Purple97Error(Exception):
    """Exception class for all Purple97 errors"""


class Purple97:
    """This class simulates the top-level behavior of the PURPLE cipher
    machine.

    """
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
        mapping is assumed; i.e. "AEIOUYBCDFGHJKLMNPQRSTVWXZ".

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
        self.sixes = switch.create_switch(switch.SIXES, switches_pos[0])
        self.twenties = [
            switch.create_switch(switch.TWENTIES_1, switches_pos[1]),
            switch.create_switch(switch.TWENTIES_2, switches_pos[2]),
            switch.create_switch(switch.TWENTIES_3, switches_pos[3]),
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
            alphabet = 'AEIOUYBCDFGHJKLMNPQRSTVWXZ'

        alphabet = alphabet.upper()
        if len(alphabet) != 26:
            raise Purple97Error("invalid alphabet length")

        # Count valid letters
        ctr = Counter(string.ascii_uppercase)
        for c in alphabet:
            if c in ctr:
                ctr[c] += 1

        # At this point if alphabet is legal, all keys in ctr must have a value
        # of 2. If any are 1, then alphabet was missing some letters. If any are
        # greater than 2, we had duplicate letters.

        if not all(v == 2 for v in ctr.values()):
            raise Purple97Error("invalid alphabet")

        self.alphabet = alphabet

    @classmethod
    def from_key_sheet(cls, switches, alphabet=None):
        """This class method allows one to construct a Purple97 using
        a shorthand notation used by US codebreakers.

        switches: must be a string of the form 'a-b,c,d-ef' where
            a - starting position of the sixes switch (1-25)
            b - starting position of the twenties switch #1 (1-25)
            c - starting position of the twenties switch #2 (1-25)
            d - starting position of the twenties switch #3 (1-25)
            e - which switch is the fast switch (1-3)
            f - which switch is the middle switch (1-3)

        Example: '9-1,24,6-23'

        Note that the starting positions here are 1-based since that is the
        notation the US codebreakers seemed to have used.

        alphabet: the daily alphabet, same format as in the __init__ function

        """
        try:
            sixes, twenties, speed = switches.split('-')
        except ValueError:
            raise Purple97Error('invalid switches string (-)')

        twenties = twenties.split(',')
        if len(twenties) != 3:
            raise Purple97Error('invalid twenties position')

        try:
            switches_pos = [int(s) - 1 for s in [sixes] + twenties]
        except ValueError:
            raise Purple97Error('switch positions must be numeric')

        if len(speed) != 2:
            raise Purple97Error('invalid switch speed settings')

        try:
            fast_switch, middle_switch = int(speed[0]), int(speed[1])
        except ValueError:
            raise Purple97Error('switch speed settings must be numeric')

        return cls(switches_pos, fast_switch, middle_switch, alphabet)
