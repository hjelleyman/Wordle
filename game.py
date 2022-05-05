import random
from enum import IntEnum
from typing import List, Tuple


class Information(IntEnum):
    """Enum class for information types for each letter in a wordle guess."""
    green = 2
    orange = 1
    black = 0

class Pattern:
    """Class for a pattern of a wordle guess."""
    def __init__(self, pattern: List[Information]):
        self.pattern = pattern

    def __str__(self):
        return ''.join(str(int(i)) for i in self.pattern)

    def from_str(self, pattern: str):
        self.pattern = [Information(int(i)) for i in pattern]

    def __int__(self):
        return int(''.join(str(int(i)) for i in self.pattern))

    def __repr__(self):
        return str(self)

    def __iter__(self):
        return iter(self.pattern)

    def __getitem__(self, index):
        return self.pattern[index]

class Game:
    def __init__(self, goal: str = None, wordlist_file_path: str = 'Words.txt') -> None:
        self.wordlist = self.get_word_list(wordlist_file_path=wordlist_file_path)
        if not goal:
            self.goal = random.choice(self.wordlist)
        else:
            self.goal = goal

    def get_information(self, word: str) -> Pattern:
        """
        Returns the information gained by making a guess.
        If a letter is in the correct place the information is green.
        If a letter is in the correct place but not in the correct position the information is orange.
        If a letter is not in the word the information is black.

        For a given letter. If there are more in the guess than in the goal,
        than make information black for any extra guesses.
        """
        # check that the guess is valid
        if not self.confirm_valid_input(guess=word):
            raise ValueError('Invalid guess: {}'.format(word))

        new_information = [Information.black] * len(word)
        # Deal with extra guesses - any extra orange guesses are black
        for i, letter in enumerate(self.goal):
            green_indices = [j for j, x in enumerate(word) if x == letter and i == j]
            orange_indices = [j for j, x in enumerate(word) if x == letter and i != j]
            n_letter_in_goal = self.goal.count(letter)
            orange_indices = orange_indices[:n_letter_in_goal - len(green_indices)]

            for j in orange_indices:
                new_information[j] = max(new_information[j], Information.orange)
            for j in green_indices:
                new_information[j] = max(new_information[j], Information.green)

        return Pattern(new_information)

    @staticmethod
    def get_word_list(wordlist_file_path: str = 'Words.txt') -> List[str]:
        """
        Returns a list of words from the wordlist file.
        """
        with open(wordlist_file_path, 'r') as f:
            wordlist = f.read().splitlines()
        return [word[1:-1] for word in wordlist[0][1:-1].split(',')]

    def confirm_valid_input(self, guess: str) -> bool:
        """
        Returns True if the guess is a valid word.
        """
        return guess in self.wordlist

    def run(self, agent) -> List[Tuple[str, List[int]]]:
        goal = self.goal
        guess = None
        info = []
        while True:
            guess = agent.get_guess(info=info)
            info.append((guess, self.get_information(word=guess)))
            if guess == goal:
                break
        return info


class agent_template:
    def __init__(self):
        self.name = "agent_template"

    def get_guess(self, info: Tuple[str, List[Information]] = None) -> str:
        return 'words'


if __name__ == '__main__':
    game = Game()
    agent = agent_template()
    game_record = game.run(agent)
    print(game_record)
