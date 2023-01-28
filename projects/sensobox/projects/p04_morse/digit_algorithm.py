from sensobox.buzzer import instance as buzzer
from time import sleep_ms

# define morse dictionary
morse_dict = {
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
    "Z": "--.."
}

# splits phrase into characters
def get_morse(phrase):
    res = "";
    for char in phrase.upper():
        res += char_to_morse(char)
    return res

# converts character to morse
# uses algorithm for digits instead of dictionary
def char_to_morse(char):
    if char.isalpha():
        return morse_dict[char] + " "
    elif char.isdigit():
        n = int(char)
        if n < 6:
            return n*"." + (5-n)*"-" + " "
        else:
            return (n-5)*"-" + (10-n)*"." + " "
    elif char == " ":
        return "/"
    else:
        return ""

# plays the code created    
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
