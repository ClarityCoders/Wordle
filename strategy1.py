import copy
from wordle import Wordle
from utils import get_word_list, save_results, word_score
import pymp

def filter_words(contains, no_letter, perfect, words):
    new_words = []
    for word in words:
        save = True
        for letter in contains:
            if letter not in word:
                save = False
                break
            else:
               indices = [i for i, c in enumerate(word) if c == letter] 
               if [i for i in indices if i in contains[letter]]:
                    save = False
                    break

        # If we still saved check for can't contain
        if save:
            for letter in no_letter:
                if letter in word:
                    save = False
                    break
        
        # If we still saved check for prefect
        if save:
            for position, letter in enumerate(perfect):
                if letter is not None:
                    if letter != word[position]:
                        save = False
                        break
        
        if save:
            new_words.append(word)
    
    return new_words

runs = 2000

results = pymp.shared.array((runs,), dtype='uint8')
final_round = pymp.shared.array((runs,), dtype='uint8')

wordle_loaded = Wordle()

with pymp.Parallel(8) as p1:
    for el in p1.range(0,runs):
        if el % 100 == 0:
            print(F"Current Game {el}")
        wordle = copy.deepcopy(wordle_loaded)
        wordle.reset()
        word_list = get_word_list()
        contains = {}
        not_in_word = []
        perfect = [None, None, None, None, None]
        
        while wordle.continue_game():
            guess = max(word_list, key=word_score)
            done, info = wordle.guess(guess)
            #print(info)
            # Update holders
            for position, letter in enumerate(info["perfect"]):
                if letter is not None:
                    perfect[position] = letter

            for char in info["contains"]:
                indices = [i for i, c in enumerate(guess) if c == char and perfect[i] != char]
                if char in contains:
                    contains[char].extend(indices)
                else:
                    contains[char] = indices

            # contains.extend(info["contains"])
            not_in_word.extend(info["not_in_word"])
            
            
            # Get our new word list
            word_list = filter_words(contains, not_in_word, perfect, word_list)
        
        if info['win']:
            results[el] = 1
            final_round[el] = wordle.guesses
        else:
            results[el] = 0
            final_round[el] = 0
    
print(f"{sum(results) / runs * 100}%")
print( sum(final_round) / len(final_round))
save_results(results, final_round, "RemoveWords")


