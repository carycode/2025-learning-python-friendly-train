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
"""
# ---- TOF


# ---- imports


# ---- code

def build_morse_dictionary(){
        
    # p. 2 of
    # https://www.itu.int/dms_pubrec/itu-r/rec/m/R-REC-M.1677-1-200910-I!!PDF-E.pdf
    morse_letters = {
        'a': '.-',
        'b': '-...',
        'c': '-.-.',
        
        
        }
    morse_digits = {
        }
    # p. 3 of
    # https://www.itu.int/dms_pubrec/itu-r/rec/m/R-REC-M.1677-1-200910-I!!PDF-E.pdf
    morse_punctuation = {
        }

}


# ---- EOF
