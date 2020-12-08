#!/usr/bin/env python
# -*- coding: utf-8 -*-

# test_machine.py
# Copyright (c) 2013 - 2014 Brian Neal
# Copyright (c) 2020 Hugh Coleman
#
# This file is part of hughcoleman/system97, a historically accurate simulator
# of the "System 97" or Type-B Cipher Machine. It is released under the MIT
# License (see LICENSE.)

import unittest

import system97.machine

import os

# This is the first part of the 14-part message which was delivered by the
# Japanese to the U.S. Government on December 7, 1941. Illegible characters are
# indicated by dashes.

samples = os.path.join(os.path.dirname(__file__), "samples")

ciphertext = None
with open(os.path.join(samples, "ciphertext"), "r") as fh:
    ciphertext = fh.read().strip()

plaintext = None
with open(os.path.join(samples, "plaintext"), "r") as fh:
    plaintext = fh.read().strip()

# check that samples are fetched
if (not plaintext) or (not ciphertext):
    raise RuntimeError("could not read plaintext/ciphertext samples")

class TestSystem97(unittest.TestCase):
    def test__encrypt(self):
        """ Ensure that System97.encrypt properly encrypts the supplied
        plaintext.
        """

        machine = system97.machine.System97(
            positions={6: 8, 20: (0, 23, 5)},
            speeds=(2, 3, 1),
            plugboard="NOKTYUXEQLHBRMPDICJASVWGZF",
        )

        self.assertEqual(ciphertext, machine.encrypt(plaintext))

    def test__decrypt(self):
        """ Ensure that System97.decrypt properly decrypts the supplied
        ciphertext.
        """

        machine = system97.machine.System97(
            positions={6: 8, 20: (0, 23, 5)},
            speeds=(2, 3, 1),
            plugboard="NOKTYUXEQLHBRMPDICJASVWGZF",
        )

        self.assertEqual(plaintext, machine.decrypt(ciphertext))
