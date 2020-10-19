#!/usr/bin/env python
# -*- coding: utf-8 -*-

# switch.py
# Copyright (c) 2013 Brian Neal
# Copyright (c) 2020 Hugh Coleman
# 
# This file is part of hughcoleman/system97, a historically accurate simulator 
# of the "System 97" or Type-B Cipher Machine. It is released under the MIT 
# License (see LICENSE.)

""" Implements a multi-layered ("multi-poled") stepping switch.

Stepping switches are capable of routing electrical signals to one of many
different output locations. This made them essential to the construction of the
Type-B machine, being responsible for performing the obfuscation of the
plaintext.

In simple, a multi-layered stepping switch is structured like this.

                                       o
                                      /
                   #                 /                     #                   
                      #  #          /                #  #                     
        Layer 1    .        #  #   /           #  #        .                        
        Layer 2    .  .  .        # # # # # #        .  .  .                       
        Layer 3    .  .  .  .  .               .  .  .  .  .
        Layer 4    .  .  .  .  .  A . . . . .  .  .  .  .  .
                      .  .  .  .  B . . . . .  .  .  .  .
                            .  .  C . . . . .  .  .
                                  D . . . . . 

Currently, an electrical signal fed into the wiper arm on layer 2 will emerge
at 'B'. However, if the arm were to step, then the signal would be diverted
elsewhere. This construction allows stepping switches to be used in performing 
monoalphabetic substitution ciphers. The outputs can be wired together to
encode a different alphabet depending on the position of the wiper arm.

Below are the substitution tables encoded into the routing_logic of the four 
stepping switches in the Type-B machine. Each row represents a layer; each 
column represents a different position of the wiper arm.

    CONSONANTS I                    CONSONANTS II    
    B  HFVDXCTBVPZGSNPKJMQBLWTGR    B  SPFHJGKZLMNCTXWZDGRKVBTXQ
    C  XGBRHNJZLKBFVPTSDQJCZSWKM    C  LHWNCVFBKPJDMTRDHSZNXGKQB
    D  RTQZKLHJNVTSMJCWGFLDPCXBF    D  BSGCQRDTJNRLSWPXFZQBHPMKV
    F  BVHFZRWTKLNCXDJBWRPFGQMSK    F  GCKZDJNMSWFMBPXCRLVHBZQTS
    G  MRSHQJLPZDCQTKFPVWZGMBNXL    G  VFTRLMXSGKWQVDBFCMGXPHNZJ
    H  FBNTGXMRWZVXCSKNQDTHVJZLP    H  XLBJFLQKCTZRDQJGPVWRSNHMF
    J  CZXKWHQGJFLHNTSVXCRJBMGPD    J  DKPWVXCRFZHSQLMNTBKGZRXJT
    K  JSPXFDBWRMFTKHXRZVMKQGLCN    K  CTSPRZLNQVBTLMHRGXFWJKGBD
    L  QDTCMWVSBRKPLFGZRNXLJXBHV    L  MXZSBKPWVGQJFHNLWQCVTLDCR
    M  LKWPDQCMTGSRJZBTNXHMSVFDZ    M  KVRDPQTGBHXNJCSMZPSDLJFWG
    N  KWMVTPGQSJMKDCNQLZBNFHPRX    N  NGQKWBMDNLPZHVGWJFTMDXSRC
    P  TNDLSKFHGWQJRGLXMBCPDZQVH    P  WNVGZCVJHDSPKRLTXCBQNFZHM
    Q  DPJGRMNKXCDVWBZLCHNQTLJFS    Q  PZNMHTRQXFGWCNKSBJLPQDVLW
    R  WQRBPSXDCTWMQLVJHPFRKNHZG    R  TJCBNDSVWXLHRFZPSHXZMQCGK
    S  SMKNJTZFHQRWPXHDBLGSWPVTC    S  HMJVTFZXRQTBGJVKLNDSCMWPN
    T  NXZMCVRLPHGDBWRFSJDTNKCQW    T  QWLXSPHFMJCGNZFJKRHTWVBDL
    V  GCFJVZKNFBHLGMQCPSWVXDRWT    V  ZBHLGNWCDBVKPSDQMTJFKWRVX
    W  PHLQNFSVMXJBZRDGTKVWCFSMJ    W  FRDTKWBLZRMVXGQHNKMCFTJSP
    X  ZLCSBGDXQSPNHVWMFGKXRTDJB    X  RQMFXHJPTSKXWBCVQDPJGSLNZ
    Z  VJGWLBPCDNXZFQMHKTSZHRKNQ    Z  JDXQMSGHPCDFZKTBVWNLRCPFH

    CONSONANTS III                  VOWELS
    B  JSCTPQFLGNXBDLKWRVMZNTHKQ    A  EYAOIEYIUOEUIOAUYEAIYAYOU
    C  XVNDWLJHRTKPFNQTBXSLZGMJC    E  AIUIYAUYOUAOAEYOEIEAUIOYE
    D  NRZPTGCFWLDVMHRSJBCKQMXGV    I  IUOEAYOAEIOYEUEIUOIYAYUAO
    F  DCPLFHSMVWSQPGTFZNRHKXTBJ    O  UEYAOUEOYEUIYAIYIAUOEOAEI
    G  ZPBFLKVWQDRLBMXCHJNPTFGSR    U  OAEYUIAUIAYEOIUAOUYEOEIUY
    H  BQXZDJMTSPGJWFPVQCHNMWLRK    Y  YOIUEOIEAYIAUYOEAYOUIUEIA
    J  MKFHSPXKNGBRCVZQTWJCWSBLD
    K  HDMXQVGRPSNCKXJPWFBGRVZTL
    L  TBLWHRKGJMCSRQMHPDTFXBVNZ
    M  PXRCZWTPKBMFQSDNLKZJHDFVG
    N  VLHGKZBVDRPGXJSZFMQTSCNWT
    P  QFSKCMPBHVTNJCLXVGDRFZWHM
    Q  KMQRJCDZBCWHTPFRGSLVBNJXH
    R  LJDNMXQSCFZTHWVGNPKDVHRZB
    S  FNJMGNHQZXVDSRBLCTWSJKQDP
    T  WZTBXSRXFHJKLZNBDLVMGQCPS
    V  GTWSRFZCLKQWVBGKMHXQDJPFN
    W  RHKVBDLNMJFXZTCJSQGXLPKCW
    X  SWGQVBNJTQLZGKHDXZPWCRDMF
    Z  CGVJNTWDXZHMNDWMKRFBPLSQX

Numerical versions of this data is available in system97.logic under names 
`SIXES`, `TWENTIES_I`, `TWENTIES_II`, and `TWENTIES_III`.

"""

class SteppingSwitch:

    def step(self):
        """ Step the wiper arm of this SteppingSwitch one position forwards, 
        looping back to zero in the case of an overflow. 
        """

        self.position = (self.position + 1) % self.size

    def encrypt(self, char):
        """ Feed the supplied character backwards through the stepping switch's
        logical network.
        """
        
        # TODO: generate inverse logic tables to ensure that this is more
        # efficient
        return {self.routing_logic[k][self.position]: k for k in self.routing_logic.keys()}[char]

    def decrypt(self, char):
        """ Feed the supplied chararacter forwards through the stepping 
        switch's logical network.
        """

        return self.routing_logic[char][self.position]
    
    def __init__(self, routing_logic, position=0, size=25):
        """ Construct a stepping switch with the given logical network. 
        
         - `routing_logic` expects a dictionary, with keys representing the 
           different layers, each associated with a list of output values.
         - `position` expects an integer specifying the initial position of the
           rotor arm.
         - `size` expects an integer specifying the number of possible arm 
           positions in the stepping switch. This defaults to 25, as this was
           the size of all four stepping switches in the original Type-B
           machine.
        
        """

        if any(size != len(vs) for vs in routing_logic.values()):
            raise ValueError(f"uneven routing_logic matrix")
        
        if (position < 0) or (size <= position):
            raise ValueError(f"cannot set stepper arm position to {position}")
        
        self.routing_logic = routing_logic
        self.position = position
        self.size = size
