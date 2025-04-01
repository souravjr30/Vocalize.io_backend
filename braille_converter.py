'''braille_dict = {
    'a': '⠁', 'b': '⠃', 'c': '⠉', 'd': '⠙', 'e': '⠑',
    'f': '⠋', 'g': '⠛', 'h': '⠓', 'i': '⠊', 'j': '⠚',
    'k': '⠅', 'l': '⠇', 'm': '⠍', 'n': '⠝', 'o': '⠕',
    'p': '⠏', 'q': '⠟', 'r': '⠗', 's': '⠎', 't': '⠞',
    'u': '⠥', 'v': '⠧', 'w': '⠺', 'x': '⠭', 'y': '⠽',
    'z': '⠵'
}

def text_to_braille(text):
    # Make sure the input is in lowercase
    text = text.lower()
    
    braille_output = ""
    
    for char in text:
        if char in braille_dict:
            braille_output += braille_dict[char]  # Append only the Braille character, no alphabet
        else:
            braille_output += " "  # Space for characters that are not in Braille (e.g., punctuation, spaces)
    
    return braille_output'''


'''braille_dict = {
    # Letters
    'a': '⠁', 'b': '⠃', 'c': '⠉', 'd': '⠙', 'e': '⠑',
    'f': '⠋', 'g': '⠛', 'h': '⠓', 'i': '⠊', 'j': '⠚',
    'k': '⠅', 'l': '⠇', 'm': '⠍', 'n': '⠝', 'o': '⠕',
    'p': '⠏', 'q': '⠟', 'r': '⠗', 's': '⠎', 't': '⠞',
    'u': '⠥', 'v': '⠧', 'w': '⠺', 'x': '⠭', 'y': '⠽',
    'z': '⠵',

    # Numbers (preceded by number sign in actual Braille)
    '1': '⠁', '2': '⠃', '3': '⠉', '4': '⠙', '5': '⠑',
    '6': '⠋', '7': '⠛', '8': '⠓', '9': '⠊', '0': '⠚',

    # Punctuation
    ',': '⠂',  # Comma
    ';': '⠆',  # Semicolon
    ':': '⠒',  # Colon
    '.': '⠲',  # Period
    '!': '⠖',  # Exclamation mark
    '?': '⠦',  # Question mark
    '\'': '⠄',  # Apostrophe
    '"': '⠶',  # Quotation mark
    '-': '⠤',  # Hyphen
    '(': '⠶',  # Open parenthesis
    ')': '⠶',  # Close parenthesis
    '/': '⠌',  # Slash
    '=': '⠿',  # Equals sign
    '*': '⠔',  # Asterisk
    ' ': ' ',   # Space (preserved as is)
    
    # Special symbols
    '#': '⠼',  # Number sign
    '&': '⠯',  # And
    '@': '⠈',  # At sign
    '$': '⠎⠎',  # Dollar sign (varies by region)
}

def text_to_braille(text):
    # Make sure the input is in lowercase
    text = text.lower()

    braille_output = ""

    for char in text:
        if char in braille_dict:
            braille_output += braille_dict[char]  # Append the Braille character
        else:
            braille_output += " "  # Space for unrecognized characters

    return braille_output

# Capital letter indicator
capital_indicator = '⠠'

def text_to_braille(text):
    braille_output = ""

    for char in text:
        if char.isupper():
            # Add capital indicator before the letter
            braille_output += capital_indicator
            char = char.lower()  # Convert to lowercase to map to Braille
        if char in braille_dict:
            braille_output += braille_dict[char]
        else:
            braille_output += " "  # Space for unrecognized characters

    return braille_output
'''

braille_dict = {
    # Lowercase Letters
    'a': '⠁', 'b': '⠃', 'c': '⠉', 'd': '⠙', 'e': '⠑',
    'f': '⠋', 'g': '⠛', 'h': '⠓', 'i': '⠊', 'j': '⠚',
    'k': '⠅', 'l': '⠇', 'm': '⠍', 'n': '⠝', 'o': '⠕',
    'p': '⠏', 'q': '⠟', 'r': '⠗', 's': '⠎', 't': '⠞',
    'u': '⠥', 'v': '⠧', 'w': '⠺', 'x': '⠭', 'y': '⠽',
    'z': '⠵',

    # Numbers (preceded by number sign)
    '1': '⠁', '2': '⠃', '3': '⠉', '4': '⠙', '5': '⠑',
    '6': '⠋', '7': '⠛', '8': '⠓', '9': '⠊', '0': '⠚',

    # Punctuation
    ',': '⠂',  # Comma
    ';': '⠆',  # Semicolon
    ':': '⠒',  # Colon
    '.': '⠲',  # Period
    '!': '⠖',  # Exclamation mark
    '?': '⠦',  # Question mark
    '\'': '⠄',  # Apostrophe
    '"': '⠶',  # Quotation mark
    '-': '⠤',  # Hyphen
    '(': '⠶',  # Open parenthesis
    ')': '⠶',  # Close parenthesis
    '/': '⠌',  # Slash
    '=': '⠿',  # Equals sign
    '*': '⠔',  # Asterisk
    ' ': ' ',   # Space (preserved as is)

    # Special Symbols
    '#': '⠼',  # Number sign
    '&': '⠯',  # And
    '@': '⠈',  # At sign
    '$': '⠎⠎',  # Dollar sign (varies by region)
}

# Capital letter and number indicators
capital_indicator = '⠠'
number_indicator = '⠼'

def text_to_braille(text):
    braille_output = ""
    is_number = False  # Track whether the last character was a number

    for char in text:
        if char.isupper():
            braille_output += capital_indicator  # Add capital indicator
            char = char.lower()  # Convert to lowercase for lookup
        
        if char.isdigit():
            if not is_number:
                braille_output += number_indicator  # Add number sign before a digit sequence
                is_number = True
            braille_output += braille_dict[char]  # Append digit in Braille
        else:
            is_number = False  # Reset number tracking when encountering non-numeric characters
            
            if char in braille_dict:
                braille_output += braille_dict[char]
            else:
                braille_output += char  # Preserve unrecognized characters (e.g., emoji)

    return braille_output

#Explanation:
#Letters: The basic Braille alphabet is included.
#Numbers: Mapped to their respective Braille cells (preceded by the number sign ⠼ in real Braille).
#Punctuation: Added common punctuation marks, including commas, periods, exclamation marks, and parentheses.
#Spaces: Spaces are preserved as is.
#This should now cover all common Grade 1 Braille characters for English text!