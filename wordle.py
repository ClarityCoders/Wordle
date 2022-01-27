#Attemting to create a simulated game of wordle
import nltk
from nltk.corpus import words
import random

class Wordle():

    def __init__(self):
        nltk.data.path.append('/work/words')
        word_list = words.words()
        self.words_five = [word.lower() for word in word_list if len(word) == 5]
        self.current_word = random.choice(self.words_five)
        self.guesses = 0
        self.win = False

    def reset(self):
        done = False
        self.current_word = random.choice(self.words_five)
        self.guesses = 0
        self.win = False
        return done, {}

    def guess(self, word):
        """
            Pass in a guess and get dictionary back.
            With Perfect, contains, not_in_word
        """
        done = False
        perfect = [None, None, None, None, None]
        contains = []
        not_in_word = []

        for position, letter in enumerate(word):
            if letter == self.current_word[position]:
                perfect[position] = letter
            elif letter not in self.current_word:
                not_in_word.append(letter)
            else:
                contains.append(letter)

        if None not in perfect:
            self.win = True
            done = True

        info = {
            'perfect': perfect,
            'contains': contains,
            'not_in_word': not_in_word,
            'win': self.win
        }

        self.guesses += 1

        return done, info

    def continue_game(self):
        if self.guesses < 6 and not self.win:
            return True
        else:
            False





if __name__ == '__main__':
    wordle = Wordle()
    print(wordle.current_word)

    while wordle.continue_game():

        info = wordle.guess(input("Please Make a guess: "))
        print(info)
        if info['win']:
            print("WE WON!")
            break