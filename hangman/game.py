from .exceptions import *
import random



class GuessAttempt(object):
    def __init__(self, letter, hit=None, miss=None):
        if hit is True and miss is True:
            raise InvalidGuessAttempt()
            
        self.letter = letter
        self.hit = hit
        self.miss = miss
        
    def is_hit(self):
        if self.hit:
            return True
        else:
            return False
    
    def is_miss(self):
        if self.miss:
            return True
        else:
            return False
        


class GuessWord(object):
    def __init__(self, word):
        self.answer = word
        self.masked = '*' * len(word)
        if word == '':
            raise InvalidWordException()
        
    def perform_attempt(self, letter):
        if len(letter) > 1:
            raise InvalidGuessedLetterException()

        if letter in self.answer or letter in self.answer.lower():
            attempt = GuessAttempt(letter, hit=True)
            guess_positions_list = []
            for index, char in enumerate(self.answer):
                if char == letter or char.lower() == letter:
                    guess_positions_list.append([index, char])
            for match in guess_positions_list:
                new_masked = self.masked[:match[0]] + match[1] + self.masked[match[0]+1:]
                self.masked = new_masked.lower()
        else:
            attempt = GuessAttempt(letter, miss=True)
        return attempt
            
    
        


class HangmanGame(object):
    WORD_LIST = ['rmotr', 'python', 'awesome']

    def __init__(self, word_list=None, number_of_guesses=5):
        if not word_list:
            word_list = self.WORD_LIST
        self.word = GuessWord(self.select_random_word(word_list))
        self.remaining_misses = number_of_guesses
        self.previous_guesses = []

    def is_won(self):
        return self.word.masked == self.word.answer

    def is_lost(self):
        return self.remaining_misses == 0

    def is_finished(self):
        return self.is_won() or self.is_lost()

    def guess(self, character):
        character = character.lower()
        if character in self.previous_guesses:
            raise InvalidGuessedLetterException()

        if self.is_finished():
            raise GameFinishedException()

        self.previous_guesses.append(character)
        attempt = self.word.perform_attempt(character)
        if attempt.is_miss():
            self.remaining_misses -= 1

        if self.is_won():
            raise GameWonException()

        if self.is_lost():
            raise GameLostException()

        return attempt

    @classmethod
    def select_random_word(cls, word_list):
        if not word_list:
            raise InvalidListOfWordsException()
        return random.choice(word_list)
