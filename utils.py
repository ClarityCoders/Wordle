import nltk
from nltk.corpus import words

letter_frequencies = {
    "e": 0.13,
    "t": 0.091,
    "a": 0.082,
    "o": 0.075,
    "i": 0.07,
    "n": 0.067,
    "s": 0.063,
    "h": 0.061,
    "r": 0.06,
    "d": 0.043,
    "l": 0.04,
    "c": 0.028,
    "u": 0.028,
    "m": 0.025,
    "w": 0.024,
    "f": 0.022,
    "g": 0.02,
    "y": 0.02,
    "p": 0.019,
    "b": 0.015,
    "v": 0.0098,
    "k": 0.0077,
    "j": 0.0015,
    "x": 0.0015,
    "q": 0.00095,
    "z": 0.00074,
}

def get_word_list():
    word_list = words.words()
    words_five = [word.lower() for word in word_list if len(word) == 5]
    return words_five

def word_score(word):
    letters_in_word = list(set(word))
    word_letter_frequencies = [letter_frequencies[letter] for letter in letters_in_word]
    word_score = sum(word_letter_frequencies)
    return word_score

def save_results(results, final_round, file_name):
    with open(f'{file_name}-Results.csv', 'w') as f:
      
        # using csv.writer method from CSV package
        for result in results:
            f.write(f"{result}\n")
    with open(f'{file_name}-Rounds.csv', 'w') as f:
      
        # using csv.writer method from CSV package
        for round in final_round:
            f.write(f"{round}\n")