#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
morse.py
Morse code translater
Created on Fri Feb 21 15:16:13 2025

@author: dc

2025-02-26: DAV: fill in some comments.
2025-02-24: A little help by Russ Hensel: text-to-dots-and-dashes now works
2025-02-21: started by David Cary.

FUTURE: automatically detect
    * ... --- ... dots and dashes
    * - - -   --- --- ---   - - - long (dashes) vs short (dots)
    * Normal ASCII text to translate into Morse
    * slashes between words (common on internet); or long gaps between words

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
https://docs.python.org/3/tutorial/appendix.html#executable-python-scripts
and
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

Related:

* Morse code decoder https://imgur.com/gallery/code-Ydr0xky
* Morse code chart https://www.reddit.com/r/codes/comments/jvmtdk/morse_code_chart_very_useful_resource/
* learn cw online (LCWO): https://lcwo.net
* online Morse code training tools and history https://morsecode.world/
* looking for app to listen to Morse code and decode it https://www.reddit.com/r/ios/comments/66mj69/app_that_can_listen_to_morse_code_and_translate_it/
* "If only the camera could read Morse code" https://www.reddit.com/r/shortcuts/comments/9hj2ol/morse_code_shortcut_that_translates_text_into/
* "Morse code Generator in Python" https://www.reddit.com/r/learnpython/comments/kr3yr9/morse_code_generator_in_python/
* "Neat site for learning Morse Code" https://www.reddit.com/r/amateurradio/comments/1cxag6t/neat_site_for_learning_morse_codethats_mostly/
* "I made a Morse code translator" (text-to-sound) https://www.reddit.com/r/Python/comments/w5balg/i_made_a_morse_code_translator/
* text-to-morse (great documentation) https://github.com/Kishanjaisoorya/Morse-code-convertor-python
* "How to decode morse code in a more pythonic way" https://stackoverflow.com/questions/71099952/how-to-decode-morse-code-in-a-more-pythonic-way
* "Morse Code Ninja - A complete Morse Code Learning Tool" https://www.reddit.com/r/amateurradio/comments/wqow80/morse_code_ninja_a_complete_morse_code_learning/

"""
# ---- TOF


# ---- imports


# ---- code

def build_morse_dictionary():
    """
    Build morse-to-text and text-to-morse dictionaries.
    """
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
        'x': '-..-',
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
    # https://www.omniglot.com/writing/morsecode.htm
    morse_punctuation = {
        '.': '.-.-.-', # period
        ',': '--..--',
        ':': '---...', # colon (or division sign?)
        '?': '..--..',
        '\'': '.----.', # apostrophe
        '-': '-....-', # hyphen or dash or subtraction sign
        '/': '-..-.', # fraction bar or division sign
        '(': '-.--.', # left-hand bracket
        ')': '-.--.-', # right-hand bracket
        '"': '.-..-.', # quotation mark (before and after)
        '=': '-...-', # "double hyphen"
        #...
        '+': '.-.-.', # cross or addition sign
        #...
        '@': '.--.-.'
        }

    # FUTURE: perhaps add the prosigns and abbreviations from
    # https://morsecode.world/international/morse.html
    # https://www.radioqth.net/morsecode
    # ?

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
    for key,value in translation_table.items():
        reverse_translation_table[value] = key

    # check for duplicates
    for key,value in translation_table.items():
        reverse_value = reverse_translation_table[value]
        if key != reverse_value:
            print( f"whoops: Morse {value} mapped to both {key} and {reverse_value} ")
    # check for duplicates
    assert len(reverse_translation_table) == len(translation_table)

    return translation_table, reverse_translation_table

def decode_from_morse( dotty_original, morse_to_text ):
        """
        decode dots-and-dashes
        into text
        using the standard International Morse code.
        """
        output = []
        # handle "·" ( &middot; ) ( Unicode : U+00B7 ) (Latin1 / Windows-1252 : 0xb7 )
        # so both '.-'and "·-" are recocognized as the letter 'a'.
        mid_dot = "\N{MIDDLE DOT}"
        dotty = dotty_original.replace( mid_dot, '.' )
        list_of_morse_characters = dotty.split(" ")
        for morse_character in list_of_morse_characters:
            assert (" " != morse_character)
            if( "" == morse_character ):
                # long gap --> space
                output += " "
            else:
                try:
                    temp = morse_to_text[morse_character]
                except KeyError:
                    print( f"unknown {morse_character = }" )
                    temp = " ### "
                output += temp
                print( f"({temp = })")
        # FIXME: support "/" as word separator

        print( f"\n\n{output = }" )
        out_string = "".join( output )
        return out_string


def encode_to_morse(text, text_to_morse):
        """
        encode normal text into dots and dashes
        using the standard International Morse code.
        """
        output = []
        for character in text:
            temp = text_to_morse[character.lower()] + ' ' # single space between letters
            print( f"\n({ temp = })")
            # output += temp # splits up strings into letters ...
            output.append(temp) # appends the string as a single item
        print( f"\n\n{output = }" )
        out_string = "".join( output )
        return out_string


def main():
        text_to_morse, morse_to_text = build_morse_dictionary()
        print( text_to_morse )
        print( morse_to_text )
        text = "Testing Morse with David and Russ"
        out_string = encode_to_morse(text, text_to_morse)
        print( f"\n\n{out_string = }" )
        print( 'done')
        dotty = "- . ... - .. -. --.    -- --- .-. ... .    .-- .. - ...."
        decoded_text = decode_from_morse( dotty, morse_to_text )
        print( f"\n{decoded_text = }" )
        dotty = ".. - .. ... .- .-- .- -.-- --- ..-. - .-. .- -. ... -- .. - - .. -. --. - . -..- - .. -. ..-. --- .-. -- .- - .. --- -. .- ... .- ... . .-. .. . ... --- ..-. --- -. -····- --- ..-. ..-. - --- -. . ... --··-- .-.. .. --. .... - ... --··-- --- .-. -.-. .-.. .. -.-. -.- ... - .... .- - -.-. .- -. -... . -.. .. .-. . -.-. - .-.. -.-- ..- -. -.. . .-. ... - --- --- -.. -... -.-- .- ... -.- .. .-.. .-.. . -.. .-.. .. ... - . -. . .-. --- .-. --- -... ... . .-. ...- . .-. .-- .. - .... --- ..- - ... .--. . -.-. .. .- .-.. . --.- ..- .. .--. -- . -. - ·-·-·-"
        decoded_text = decode_from_morse( dotty, morse_to_text )
        print( f"\n{decoded_text = }" )


        # FIXME: round-trip encode-decode cycle.


main()



# ---- EOF
