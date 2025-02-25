#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
morse.py
Morse code translater
Created on Fri Feb 21 15:16:13 2025

@author: dc

2025-02-21: started by David Cary.

FUTURE: automatically detect
    * ... --- ... dots and dashes
    * - - -   --- --- ---   - - - long (dashes) vs short (dots)
    * Normal ASCII text to translate into Morse

FUTURE:
    handle standard Morse code abbreviations and prosigns
    https://en.wikipedia.org/wiki/Morse_code_abbreviations
    https://en.wikipedia.org/wiki/Prosigns_for_Morse_code
    such as
    73 	Best regards
    
FUTURE:
    consider making sounds
    consider listening to sounds

FUTURE: collect these functions into a cohesive "class Morse" ?


The recommendation of
https://peps.python.org/pep-0263/
*seems* to say first or second line is
    # -*- coding: utf-8 -*-
As recommended by
https://stackoverflow.com/questions/6908143/should-i-put-shebang-in-python-scripts-and-what-form-should-it-take
the first line is the recommended shebang line
    #!/usr/bin/env python3
(this *must* be the first line,
so the "utf-8" line, if any, must be the second line
).
However,
https://peps.python.org/pep-0008/
suggests
"Code ... should always use UTF-8, and should not have an encoding declaration."

"""
# ---- TOF


# ---- imports


# ---- code

def build_morse_dictionary():
        
    # p. 2 of
    # https://www.itu.int/dms_pubrec/itu-r/rec/m/R-REC-M.1677-1-200910-I!!PDF-E.pdf
    morse_letters = {
        'a': '.-',
        'b': '-...',
        'c': '-.-.',
        'd': '-..',
        'e': '.',
        'accented e': '..-..',
        'f': '..-.',
        'g': '--.',
        'h': '....',
        
        'i': '..',
        'j': '.---',
        'k': '-.-',
        'l': '.-..',
        'm': '--',
        'n': '-.',
        'o': '---',
        'p': '.--.',
        'q': '--.-',
        'r': '.-.',
        's': '...',
        't': '-',
        'u': '..-',
        'v': '...-',
        'w': '.--',
        'x': '.--',
        'y': '-.--',
        'z': '--..',
        }
    morse_digits = {}
    for digit in range(1,5):
        dots = digit
        dashes = 5-dots
        morse_digits[str(dots)] = (
            '.'*dots + '-'*dashes
            )
    for digit in range(5,10):
        dashes = digit - 5
        dots = 5-dashes
        morse_digits[str(digit)] = (
            '-'*dashes + '.'*dots
            )
    morse_digits['0'] = '-'*5
    # p. 3 of
    # https://www.itu.int/dms_pubrec/itu-r/rec/m/R-REC-M.1677-1-200910-I!!PDF-E.pdf
    morse_punctuation = {
        '.': '.-.-.-', # period
        '?': '..--..',
        '@': '.--.-.'
        }
    
    # misc other stuff not exactly called out
    morse_other = {
        ' ': '  ' # two spaces here, so we end up with a net 3 spaces between words
        }

    translation_table = {}
    translation_table.update(morse_letters)
    translation_table.update(morse_digits)
    translation_table.update(morse_punctuation)
    translation_table.update(morse_other)
    
    reverse_translation_table = {}
    # FIXME
    
    return translation_table, reverse_translation_table


def main():
        table, reverse_table = build_morse_dictionary()
        print( table )
        text = "Testing Morse with David and Russ"
        output = []
        for character in text:
            temp = table[character.lower()] + ' ' # single space between letters
            print( f"\n({ temp = })")
            # output += temp # splits up strings into letters ...
            output.append(temp) # appends the string as a single item
        print( f"\n\n{output = }" )
        out_string = "".join( output )
        
        print( f"\n\n{out_string = }" )
        print( 'done')

main()


# ---- EOF
