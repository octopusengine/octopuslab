from sensobox.buzzer import instance as buzzer
from time import sleep_ms

# define morse dictionary
MORSE_DICT = {
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    "0": "-----",
}

# splits phrase into characters
def get_morse(phrase):
    res = "";
    for char in phrase.upper():
        res += char_to_morse(char)
    return res

# converts character to morse using MORSE_DICT
def char_to_morse(char):
    if char.isalpha() or char.isdigit():
        return morse_dict[char] + " "
    elif char == " ":
        return "/"
    else:
        return ""

# use buzzer to play morse code created    
def play_morse(code):
    for char in code:
        if char == "-":
            buzzer.play_tone(500, 4, 100)
            sleep_ms(100)
        elif char == ".":
            buzzer.play_tone(500, 16, 100)
            sleep_ms(100)
        elif char == " ":
            sleep_ms(300)
        else:
            sleep_ms(600)
            
print(play_morse(get_morse("ahoj")))
