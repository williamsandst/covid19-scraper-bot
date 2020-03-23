

def match(string, sequence):
    """Finds the first matching wildcard {} from sequence in string """
    words = string.split()
    words = combine_separate_numbers(words)
    sequence = sequence.split()

    wildcard_index = -1
    for i, word in enumerate(words):
        for j, match_word in enumerate(sequence):
            if match_word == "{}":
                wildcard_index = i+j
                continue
            elif words[i+j] != match_word:
                wildcard_index = -1
                break
        if wildcard_index != -1:
            break
    
    if wildcard_index == -1:
        print("Function <match()>: The supplied string does not match the sequence ", sequence)
    return words[wildcard_index]
            
                

def combine_separate_numbers(words):
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
    return processed_words