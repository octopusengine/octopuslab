# note lenght: 2 > 1/2, 4 > 1/4, 8 > 1/8 ...

from sensobox.notes import *

#old
mario = [E7, E7, 0, E7, 0, C7, E7, 0, G7, 0, 0, 0, G6, 0, 0, 0, C7, 0, 0, G6, 0, 0, E6, 0, 0, A6, 0, B6, 0, AS6, A6, 0, G6, E7, 0, G7, A7, 0, F7, G7, 0, E7, 0,C7, D7, B6, 0, 0, C7, 0, 0, G6, 0, 0, E6, 0, 0, A6, 0, B6, 0, AS6, A6, 0, G6, E7, 0, G7, A7, 0, F7, G7, 0, E7, 0,C7, D7, B6, 0, 0]

# new format:
alert1 = [[A5,16], [0,8], [A5,16], [0,8], [A5,16], [0,1]]
alert2 = [[E7,8], [C7,8], [E7,8], [0,2], [E7,8], [C7,8], [E7,8], [0,1]]
alert3 = [[G7,2], [C7,2], [E7,8], [0,1]]

jingle1 = [[C6,4], [0,4], [C5,8], [0,8], [C6,8]]
jingle2 = [[C5,2], [0,16], [C5,2], [0,16], [G5,8]]

# jingle10 = [[C5,4], [G4,8], [G4,8], [A4,4], [G4,4], [0,4], [B4,4], [C5,4]]
jingle10 = [[C5,4], [C5,16], [0,16], [G4,8], [G4,8], [A4,4], [G4,4], [0,4], [B4,4], [0,16], [C5,4]]


starw1 = [[F5,4], [0,4], [F5,4], [0,4], [F5,4], [0,4], [C5,4], [0,8], [GS5,8], [0,16], [F5,4], [0,4], [C5,4], [0,8], [GS5,8], [0,16], [F5,4], [0,1]]

#  piezzo.play_melody(indiana,70,32)
indiana = [[E5,4],[0,16],[F5,8],[G5,8],[0,16],[C6,2],[0,2],[0,4],[D5,4],[0,16],[E5,8],[F5,2],[0,2],[0,4],[G5,4],[0,16],[A5,8],[B5,8],[0,16],[F6,2],[0,2],[A5,4],[0,16],[B5,8],[C6,4],[0,4],[D6,4],[0,4],[E6,4]]

#  piezzo.play_melody(canon_d,30,32)
canon_d = [[A6,8],[FS6,16],[G6,16],[A6,8],[FS6,16],[G6,16],[A6,16],[A5,16],[B5,16],[CS6,16],[D6,16],[F6,16],[FS6,16],[G6,16],[FS6,8],[D6,16],[E6,16],[FS6,8],[FS5,16],[G5,16],[A5,16],[B5,16],[A5,16],[G5,16],[A5,16],[FS5,16],[G5,16],[A5,16],[G5,8],[B5,16],[A5,16],[G5,8],[FS5,16],[E5,16],[FS5,16],[E5,16],[D5,16],[E5,16],[FS5,16],[G5,16],[A5,16],[B5,16],   [G5,8],[B5,16],[A5,16],[B5,8],[CS6,16],[D6,16],[A5,16],[B5,16],[CS6,16],[D6,16],[E6,16],[FS6,16],[G6,16],[A6,16]]

# pirates = []
"""
pirates = [[D4,8], [D4,8], [D4,8], [D4,8], [D4,8], [D4,8], [D4,8], [D4,8],[D4,8], [D4,8], [D4,8], [D4,8], [D4,8], [D4,8], [D4,8], [D4,8], [D4,8], [D4,8], [D4,8], [D4,8],[D4,8], [D4,8], [D4,8], [D4,8]]
pirates2 = [[A3,8], [C4,8], [D4,8], [D4,8], [D4,8], [E4,8], [F4,8], [F4,8], [F4,8], [G4,8], [E4,8], [E4,8], [D4,8], [C4,8], [C4,8], [D4,8], [0,8], [A3,8], [C4,8], [B3,8], [D4,8], [B3,8], [E4,8], [F4,8], [F4,8], [C4,8], [C4,8], [C4,8], [C4,8]] 

[D4,8], [C4,8],[D4,8], [0,8], [0,8], [A3,8], [C4,8], [D4,8], [D4,8], [D4,8], [F4,8], [G4,8], [G4,8], [G4,8], [A4,8], [A4,8], [A4,8], [A4,8], [G4,8],[A4,8], [D4,8], 0,8], [D4,8], [E3,8], [F4,8], [F4,8], [G4,8], [A4,8], [D4,8], [0,8], [D4,8], [F4,8], [E4,8], [E4,8], [F4,8], [D4,8]]
"""
