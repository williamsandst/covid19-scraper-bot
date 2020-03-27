
import dateutil.parser
import datetime

number_cleanup_dict = {ord('.'): None, ord(','): None, ord('*'): None, ord('^'): None, ord(' '): None, ord(u"\xa0"): None}

text_cleanup_dict = {ord('\n'): " ", ord('\xa0'): ' ', ord('\t'): ' '}

date_cleanup_dict = {}

date_keep_set = {"monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "pm", "am", 
    "january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"
    "mon", "tue", "wed", "thu", "fri", "sat", "sun", "jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"}

date_junk_words = {"2020", "kl.", "kl"}

date_replace_dict = {"марта": "march", "апреля":"april", "мая": "may", "mars": "march"}

def clean_number(number : str) -> int:
    number = number.strip().translate(number_cleanup_dict)
    final_number = ""
    for character in number:
        if character.isdigit():
            final_number += character
    if final_number != "":
        return int(final_number)
    else:
        return 0

def clean_if_number(words: str) -> str:
    for i, word in enumerate(words):
        is_number = True
        for char in word:
            if char.isdigit() or char == "," or char == ".":
                continue
            else:
                is_number = False
                break
        if is_number and word != "":
            words[i] = str(clean_number(word))
    return words

def date_formatter(date: str) -> datetime.datetime:
    "Uses dateutil to convert arbitary time string to datetime. Probably doesn't work with non-english months/days"
    #Keep all numbers, months, days
    date = date.strip(".,:*<>")
    if "." in date and ":" not in date:
        date = date.translate({ord(","): None, ord("."): ":"})
    end_string = ""
    has_digits = False

    words = date.split()
    new_words = list()
    for word in words: #Translate certain important words if needed
        if word in date_replace_dict:
            new_words.append(date_replace_dict[word])
        else:
            new_words.append(word)

    for word in new_words:
        if word.lower() in date_keep_set:
            end_string += word + " "
        else:
            for letter in word: #Keep words in the set
                if letter.isdigit():
                    has_digits = True
                    break
            if has_digits: #Also keep any word with a number in
                end_string += word + " "
                has_digits = False

    return dateutil.parser.parse(end_string.strip())

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
        raise TypeError
    return words[wildcard_index]

def clean_text(text: str) -> str:
    return text.translate(text_cleanup_dict)

def expand_index_by_words(string: str, index: int, words: int) -> tuple: #Expands index left and right symmetrically by x words
    #for i in range(min(index, len(string) - index))
    return False

def find_index(string: str, sequence: str) -> tuple:
    """Finds the first matching string"""
    start_index = -1
    end_index = -1
    for i, char in enumerate(string):
        if i > (len(string) - len(sequence)):
            break
        for j, seq_char in enumerate(sequence):
            if seq_char == string[i+j]:
                end_index = i+j
                continue
            else:
                end_index = -1
                break
        if end_index != -1: #Found matching sequence
            start_index = i
            break
    return (start_index, end_index)

def find_word_index(words: list, word: str):
    candidates = []
    for i, word2 in enumerate(words):
        if word2 == word:
            candidates.append(i)
    for i in candidates:
        if i > 0 and i < len(words):
            return i
    return -1

def is_time(word:str) -> bool:
    #Time nn:.nn, n:.nn, any month, 2020
    if word in date_keep_set or word in date_junk_words:
        return True
    if (len(word) > 3):
        if word[0].isdigit() and (word[2] == '.' or word[2] == ':') and word[3].isdigit():
            return True
        elif word[0].isdigit() and (word[1] == '.' or word[1] == ':') and word[2].isdigit():
            return True
    return False

def is_javascript(word: str) -> bool:
    return ("px" in word) or ("box-shadow" in word) or ("}" in word) + ("{" in word) or ("rgb" in word) or ("→" in word)

def remove_time(words: list) -> list: #Only works with words that are tuples (word, distance)
    new_words = []
    for word in words:
        if not is_time(word):
            new_words.append(word)
    return new_words

def remove_javascript(words: list) -> list:
    new_words = []
    for word in words:
        if not is_javascript(word):
            new_words.append(word)
    return new_words

def get_surrounding_words(words: list, index: int, count: int) -> list:
    return words[index-count:index] +  words[index+1:index+count+1]

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

def divide_numbers(words: list) -> list:
    """ Divide numbers joined with letters"""
    final_words = []
    tempstr = ""
    is_number = False
    for word in words:
        if not is_time(word) and not word.isdigit():
            tempstr = ""
            for char in word:
                if char.isdigit() or char == "." or char == ",": #We have a number here
                    if not is_number:
                        if tempstr != "":
                            final_words.append(tempstr)
                        tempstr = ""
                        is_number = True
                else:
                    if is_number:
                        if tempstr != "":
                            final_words.append(tempstr)
                        tempstr = ""
                        is_number = False
                tempstr += char
            if tempstr != "":
                final_words.append(tempstr)
            is_number = False
        else:
            final_words.append(word)
    return final_words
