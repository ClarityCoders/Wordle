from wordle import Wordle
from utils import get_word_list, save_results, word_score

def filter_words(contains, no_letter, perfect, words):
    new_words = []
    for word in words:
        save = True
        for letter in contains:
            if letter not in word:
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

results = []
final_round = []
wordle = Wordle()

while len(results) < 100000:
    wordle.reset()
    word_list = get_word_list()
    contains = []
    not_in_word = []
    perfect = [None, None, None, None, None]
    
    while wordle.continue_game():
        guess = max(word_list, key=word_score)
        done, info = wordle.guess(guess)
        #print(info)
        # Update holders
        contains = contains + info["contains"]
        not_in_word = not_in_word + info["not_in_word"]
        for position, letter in enumerate(info["perfect"]):
            if letter is not None:
                perfect[position] = letter
        
        # Get our new word list
        word_list = filter_words(contains, not_in_word, perfect, word_list)
    
    if info['win']:
        results.append(1)
        final_round.append(wordle.guesses)
    else:
        results.append(0)
    
print(sum(results))
print( sum(final_round) / len(final_round))
save_results(results, final_round, "RemoveWords")


