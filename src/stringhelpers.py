

number_cleanup_dict = {ord('.'): None, ord(','): None, ord('*'): None, ord('^'): None, ord(' '): None, ord(u"\xa0"): None}

def clean_number(number : str) -> int:
    number = number.strip().translate(number_cleanup_dict)
    if not number.isdigit():
        print("Error converting number string to number literal: ", number)
        raise TypeError
        return -1
    return int(number)



def match(string: str, sequence: str) -> str:
    """Finds the first matching wildcard {} from sequence in string. Ignores {$} """
    words = string.split()
    words = combine_separate_numbers(words)
    sequence = sequence.split()

    wildcard_index = -1
    for i, word in enumerate(words):
        if i > (len(words) - len(sequence)):
            break
        for j, match_word in enumerate(sequence):
            if match_word == "{}":
                wildcard_index = i+j
                continue
            elif match_word == "{$}":
                continue
            elif words[i+j] != match_word:
                wildcard_index = -1
                break
        if wildcard_index != -1:
            break
    
    if wildcard_index == -1:
        print("Function <match()>: The supplied string does not match the sequence ", sequence)
    return words[wildcard_index]
            
                

def combine_separate_numbers(words: list) -> list:
    """ Combines separated numbers eg 2 016 into 2016. Doesn't work for negative numbers, floats or exponentials """
    processed_words = list()
    number_word = "" #Temp variable for holding the combined number
    for word in words:
        if word.isdigit():
            number_word += word
        else:
            if number_word != "":
                processed_words.append(number_word)
                number_word = ""
            processed_words.append(word)
    if number_word != "":
        processed_words.append(number_word)
    return processed_words