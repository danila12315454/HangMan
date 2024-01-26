import random
from enum import Enum
from typing import Optional

import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style

DEBUG = False
success_code = 200
request_timeout = 1000


class Source(Enum):
    """Enum that represents switch between local and web word parsing."""

    FROM_FILE = 0
    FROM_INTERNET = 1


def print_wrong(text: str) -> None:
    """
    Print styled text(red).

    :parameter text: text to print.
    """
    text_to_print = Style.RESET_ALL + Fore.RED + text
    print(text_to_print)


def print_right(text: str) -> None:
    """
    Print styled text(red).

    :parameter text: text to print.
    """
    print(Style.RESET_ALL + Fore.GREEN + text)


def parse_word_from_local() -> str:
    """
    Parse word from local file.

    :returns str: string that contains the word.
    """
    try:
        with open('./src/hangman/local_words.txt', encoding='utf8') as words_file:
            return random.choice(words_file.read().split('\n'))
    except FileNotFoundError:
        return 'default'


def parse_word_from_site() -> Optional[str]:
    """
    Parse word from website.

    :return Optional[str]: string that contains the word.

    """
    url: str = 'https://randomword.com'
    page: requests.Response = requests.get(url, timeout=request_timeout)
    if page.status_code == success_code:
        soup = BeautifulSoup(page.text, 'html.parser')
        return soup.find('div', id='random_word').text
    return None


class MainProcess(object):
    """Manages game process."""

    def __init__(self, source: Enum) -> None:
        """
        Init MainProcess object.

        :parameter source: Represents source to get word.
        """
        self._source = source
        self._answer_word = ''
        self._word_string_to_show = ''
        self._guess_attempts_coefficient = 2

    def get_word(self) -> str:
        """
        Parse word(wrapper for local and web parse).

        :returns str: string that contains the word.
        :raises AttributeError: Not existing enum
        """
        if self._source == Source.FROM_INTERNET:
            word = parse_word_from_site()
            if word:
                return word
            return parse_word_from_local()
        elif self._source == Source.FROM_FILE:
            return parse_word_from_local()
        source_string = str(self._source)
        raise AttributeError(f'Non existing enum {source_string}')

    def user_lose(self) -> None:
        """Print text for end of game and exits."""
        print_wrong(f"YOU LOST(the word was '{self._answer_word}')")
        print(Style.RESET_ALL)
        exit(0)

    def user_win(self) -> None:
        """Print text for end of game and exits."""
        print_wrong(f'{self._word_string_to_show} YOU WON')
        print(Style.RESET_ALL)
        exit(0)

    def game_process(self, user_character: str) -> None:
        """
        Process user input.

        :parameter user_character: User character.
        """
        if user_character in self._answer_word:
            word_list_to_show = list(self._word_string_to_show)
            for index, character in enumerate(self._answer_word):
                if character == user_character:
                    word_list_to_show[index] = user_character
            self._word_string_to_show = ''.join(word_list_to_show)
        else:
            print_wrong('There is no such character in word')
        if self._answer_word == self._word_string_to_show:
            self.user_win()

    def start_game(self) -> None:
        """Start main process of the game."""
        with open('./src/hangman/text_images.txt', encoding='utf8') as text_images_file:
            print_wrong(text_images_file.read())
        print_wrong('Start guessing...')
        self._answer_word = self.get_word()
        self._word_string_to_show = '_' * len(self._answer_word)
        attempts_amount = int(self._guess_attempts_coefficient * len(self._answer_word))
        if DEBUG:
            print(self._answer_word)
        for attempts in range(attempts_amount):
            user_remaining_attemps = attempts_amount - attempts
            print_right(f'You have {user_remaining_attemps} more attempts')
            print_right(f'{self._word_string_to_show} enter a character to guess: ')
            user_character = input().lower()
            self.game_process(user_character)
        self.user_lose()


if __name__ == '__main__':
    main_process = MainProcess(Source(1))
    main_process.start_game()
