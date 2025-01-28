braille_dict = {
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
    
    return braille_output