#!/usr/bin/env python
# -*- coding: utf-8 -*-

# test_machine.py
# Copyright (c) 2013 - 2014 Brian Neal
# Copyright (c) 2020 Hugh Coleman
# 
# This file is part of hughcoleman/purple, a historically accurate simulator of
# the PURPLE (Type-B) Cipher Machine. It is released under the MIT License (see
# LICENSE.)

import unittest

from purple.machine import Purple97, Purple97Error
from purple.switch import SteppingSwitchError

import string

# This is the first part of the 14-part message which was delivered by the 
# Japanese to the U.S. Government on December 7, 1941. Illegible characters are
# indicated by dashes.

ciphertext = "ZTXODNWKCCMAVNZXYWEETUQTCIMNVEUVIWBLUAXRRTLVARGNTPCNOIUPJLCIVRTPJKAUHVMUDTHKTXYZELQTVWGBUHFAWSHULBFBHEXMYHFLOWD-KWHKKNXEBVPYHHGHEKXIOHQHUHWIKYJYHPPFEALNNAKIBOOZNFRLQCFLJTTSSDDOIOCVT-ZCKQTSHXTIJCNWXOKUFNQR-TAOIHWTATWVHOTGCGAKVANKZANMUINYOYJFSRDKKSEQBWKIOORJAUWKXQGUWPDUDZNDRMDHVHYPNIZXBGICXRMAWMFTIUDBXIENLONOQVQKYCOTVSHVNZZQPDLMXVNRUUNQFTCDFECZDFGMXEHHWYONHYNJDOVJUNCSUVKKEIWOLKRBUUSOZUIGNISMWUOSBOBLJXERZJEQYQMTFTXBJNCMJKVRKOTSOPBOYMKIRETINCPSQJAWVHUFKRMAMXNZUIFNOPUEMHGLOEJHZOOKHHEEDNIHXFXFXGPDZBSKAZABYEKYEPNIYSHVKFRFPVCJTPTOYCNEIQBFEXMERMIZLGDRXZORLZFSQYPZFATZCHUGRNHWDDTAIHYOOCOODUZYIWJROOJUMUIHRBEJFONAXGNCKAOARDIHCDZKIXPR--DIMUWOMHLTJSOUXPFKGEPWJOMTUVKMWRKTACUPIGAFEDFVRKXFXLFGURDETJIYOLKBHZKXOJDDOVRHMMUQBFOWRODMRMUWNAYKYPISDLHECKINLJORKWNWXADAJOLONOEVMUQDFIDSPEBBPWROFBOPAZJEUUSBHGIORCSUUQKIIEHPCTJRWSOGLETZLOUKKEOJOSMKJBWUCDDCPYUUWCSSKWWVLIUPKYXGKQOKAZTEZFHGVPJFEWEUBKLIZLWKKOBXLEPQPDATWUSUUPKYRHNWDZXXGTWDDNSHDCBCJXAOOEEPUBPWFRBQSFXSEZJJYAANMG-WLYMGWAQDGIVNOHKOUTIXYFOKNGGBFGANPWTUYLBEFFKUFLEXOIUUANVMMJEQUSFHFDOHQLAKWTBYYYLNTLYTSXCGKCEEWQRYAVGRKXIANPXNOFVXGKJFAVKLTHOCXCIVKOLXTJTUNCLQCICRUIIWQDDMOTPRVTJKKSKFHXFKMDIKIZWROGZJYMTMNOVMFJ-OKTEIVMYANOHNNYPDLEXCFRRNEBLMNYEBGNHCZZCFNWGGRHRIUUTTILKLODUYZKQOZMMNHASXHLPVTNGHQDAJIUGOOSZ-----ZRTGWFBLKI--------YBDABJ-----WYOEANV---OM"
plaintext  = "FOVTATAKIDASINIMUIMINOMOXIWOIRUBESIFYXXFCKZZRDXOOVBTNFYXFAEMEMORANDUMFIOFOVOOMOJIBAKARIFYXRAICCYLFCBBCFCTHEGOVE-NMENTOFJAPANLFLPROMPTEDBYAGENUINEDESIRETOCOMETOANAMICABLEUNDERSTANDIN-WITHTHEGOVERNMENTOFTHE-NITEDSTATESINORDERTHATTHETWOCOUNTRIESBYTHEIRJOINTEFFORTSMAYSECURETHEPEACEOFTHEPACIFICAREAANDTHEREBYCONTRIBUTETOWARDTHEREALIZATIONOFWORLDPEACELFLHASCONTINUEDNEGOTIATIONSWITHTHEUTMOSTSINCERITYSINCEAPRILLASTWITHTHEGOVERNMENTOFTHEUNITEDSTATESREGARDINGTHEADJUSTMENTANDADVANCEMENTOFJAPANESEVVFAMERICANRELATIONSANDTHESTABILIZATIONOFTHEPACIFICAREACFCCCFTHEJAPANESEQOVERNMENXHASTHEHONORTOSTATEFRANKLYITSVIEWSCONCERNINGTHECLAIMSTHEAM--VCANGOVERNMENTHASUERSISTENTLYMAINTAINEDASWELLASTHEMEASURESTHEUNITEDSTATESANDGREATBRITAINHAVETAKENTOWARDJAPANDURINGTHKSEEIGHTMONTHSCYCCCFLFCDDCFCITISTHEIMMUTABLXPOLWCYOFTHEJAPANESEGOVERNMENTTOINSURETHESTABILITYOFEASTASIAANDTOPROMOTEWORLZPEACELFLANDTHEREBYTOEIABLEALLNATIONSTOFINDEACHITSPROPERPLACEINTHEWORLDCFCCCFEVERSINCETHE-HINAAFFAIRBROKEOUTOWINGTOTHEFAILUREONTHEPARTOFCHINATOCOMPREHENLJAPANVCFSTRUEYNTENTIONSLFLTWEJAPANESEGOVERNMENTHASSTRIVENFORTHERESTORATIONOFPEACEANDIMHASCONSISTENTLYEXERTEDITSBESTEFFORTSTOPREV-NTTHEEXTENTIONOFWARVVFLIKEVISTURBANCESCFCNSIASALSOTOTHATENDTNATINSEPTEMBERLASTYEARJAPANCONCL-----HETRIPAITI--------THGERM-----DYTALYC---OV"

class TestPurple97(unittest.TestCase):

    def test_construction(self):
        Purple97()
        Purple97([0, 1, 2, 3])
        Purple97([0, 1, 2, 3], 1)
        Purple97([0, 1, 2, 3], 2, 1)
        Purple97((0, 1, 2, 3), 2, 1, string.ascii_uppercase)
        Purple97((0, 1, 2, 3), 2, 1, string.ascii_lowercase)
        Purple97(alphabet=string.ascii_lowercase)
        Purple97(fast_switch=3, middle_switch=1)

    def test_construct_bad_positions(self):
        self.assertRaises(Purple97Error, Purple97, [])
        self.assertRaises(Purple97Error, Purple97, [1])
        self.assertRaises(Purple97Error, Purple97, [1, 1, 1, 1, 1])
        self.assertRaises(SteppingSwitchError, Purple97, [1, 1, 1, 100])

    def test_construct_bad_switches(self):
        self.assertRaises(Purple97Error, Purple97, fast_switch=0)
        self.assertRaises(Purple97Error, Purple97, fast_switch=4)
        self.assertRaises(Purple97Error, Purple97, fast_switch=-1)

        self.assertRaises(Purple97Error, Purple97, middle_switch=0)
        self.assertRaises(Purple97Error, Purple97, middle_switch=4)
        self.assertRaises(Purple97Error, Purple97, middle_switch=-1)

        self.assertRaises(Purple97Error, Purple97, fast_switch=2)
        self.assertRaises(Purple97Error, Purple97, fast_switch=1, 
            middle_switch=1)
        self.assertRaises(Purple97Error, Purple97, fast_switch=2, 
            middle_switch=2)
        self.assertRaises(Purple97Error, Purple97, fast_switch=3, 
            middle_switch=3)

        self.assertRaises(Purple97Error, Purple97, fast_switch=0, 
            middle_switch=1)
        self.assertRaises(Purple97Error, Purple97, fast_switch=0, 
            middle_switch=0)
        self.assertRaises(Purple97Error, Purple97, fast_switch=0, 
            middle_switch=4)

    def test_construct_bad_alphabet(self):
        alphabets = [
            "",
            "1",
            "!" * 26,
            "DEFGHIJKLMNOPQRSTUVWXYZ",
            "ABCDEFGHIJKLMNOPQRSTUVWXYZEFGHIJ",
            "ABCDEFGHIJKLMABCDEFGHIJKLM",
            "M" * 26
        ]

        for alphabet in alphabets:        
            self.assertRaises(Purple97Error, Purple97, alphabet=alphabet)

    def test_from_key_sheet(self):
        Purple97.from_key_sheet("9-1,2,3-23")
        Purple97.from_key_sheet("1-1,1,1-13")
        Purple97.from_key_sheet("25-25,25,25-31")
        Purple97.from_key_sheet("5-20,7,18-21", alphabet=string.ascii_uppercase)

    def test_bad_from_key_sheet(self):
        self.assertRaises(SteppingSwitchError, Purple97.from_key_sheet, "0-1,2,3-13")
        self.assertRaises(SteppingSwitchError, Purple97.from_key_sheet, "26-1,2,3-13")
        self.assertRaises(SteppingSwitchError, Purple97.from_key_sheet, "1-1,0,3-13")
        self.assertRaises(SteppingSwitchError, Purple97.from_key_sheet, "1-1,2,26-13")
        self.assertRaises(SteppingSwitchError, Purple97.from_key_sheet, "1-1,2,26-03")
        self.assertRaises(SteppingSwitchError, Purple97.from_key_sheet, "1-1,2,26-00")
        self.assertRaises(SteppingSwitchError, Purple97.from_key_sheet, "1-1,2,26-14")

        self.assertRaises(Purple97Error, Purple97.from_key_sheet, "bad string")
        self.assertRaises(Purple97Error, Purple97.from_key_sheet, "1-2-1,2,26-14")
        self.assertRaises(Purple97Error, Purple97.from_key_sheet, "a-9,2,20-13")
        self.assertRaises(Purple97Error, Purple97.from_key_sheet, "1-a,2,20-13")
        self.assertRaises(Purple97Error, Purple97.from_key_sheet, "1-9,a,20-13")
        self.assertRaises(Purple97Error, Purple97.from_key_sheet, "1-9,2,a-13")
        self.assertRaises(Purple97Error, Purple97.from_key_sheet, "1-9,2,20-a3")
        self.assertRaises(Purple97Error, Purple97.from_key_sheet, "1-9,2,20-1a")
        self.assertRaises(Purple97Error, Purple97.from_key_sheet, "1-9,2,20-123")

    def test_decrypt_part_1_message(self):
        self.assertEqual(len(ciphertext), len(plaintext))

        machine = Purple97.from_key_sheet(
            switches="9-1,24,6-23",
            alphabet="NOKTYUXEQLHBRMPDICJASVWGZF")

        self.assertEqual(plaintext, machine.decrypt(ciphertext))

    def test_encrypt_part_1_message(self):
        self.assertEqual(len(ciphertext), len(plaintext))

        machine = Purple97.from_key_sheet(
            switches="9-1,24,6-23",
            alphabet="NOKTYUXEQLHBRMPDICJASVWGZF")

        # substitute illegible characters with "X"s.
        plaintext_ = plaintext.replace("-", "X")

        mismatches = 0
        for ct, ept in zip(ciphertext, machine.encrypt(plaintext_)):
            if ct != ept and ct != "-":
                mismatches = mismatches + 1

        self.assertTrue(mismatches <= 0)
