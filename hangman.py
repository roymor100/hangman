from colorama import Style, Fore
import logging

MAX_TRIES = 6


WELCOME_LOGO = r"""
    _    _
   | |  | |
   | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __
   |  __  |/ _' | '_ \ / _' | '_ ' _ \ / _' | '_ \
   | |  | | (_| | | | | (_| | | | | | | (_| | | | |
   |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                        __/ |
                        |___/"""


GAME_OVER = r"""
  __ _   __ _  _ __ ___    ___     ___  __   __  ___  _ __ 
 / _` | / _` || '_ ` _ \  / _ \   / _ \ \ \ / / / _ \| '__|
| (_| || (_| || | | | | ||  __/  | (_) | \ V / |  __/| |   
 \__, | \__,_||_| |_| |_| \___|   \___/   \_/   \___||_|   
  __/ |                                                    
 |___/ """


WINNER = r"""
 __      __  ___   _  _   _  _   ___   ___ 
 \ \    / / |_ _| | \| | | \| | | __| | _ \
  \ \/\/ /   | |  | .` | | .` | | _|  |   /
   \_/\_/   |___| |_|\_| |_|\_| |___| |_|_\
"""


HANGMAN_PHOTOS = {
    0: r"""    x-------x""",
    1: r"""    x-------x
    |
    |
    |
    |
    |""",
    2: r"""    x-------x
    |       |
    |       0
    |
    |
    |""",
    3: r"""    x-------x
    |       |
    |       0
    |       |
    |
    |""",
    4: r"""    x-------x
    |       |
    |       0
    |      /|\
    |
    |""",
    5: r"""    x-------x
    |       |
    |       0
    |      /|\
    |      /
    |""",
    6: r"""    x-------x
    |       |
    |       0
    |      /|\
    |      / \
    |"""
}


def print_logo():
    """Prints the game's logo and the max tries for the player
    :return: None
    """
    print(WELCOME_LOGO)
    print(MAX_TRIES)


def check_win(secret_word: str, old_letters_guessed: list) -> bool:
    """
    Checks if the player guessed all the letters contained in the secret word
    :param secret_word: The secret word chosen according to the index number
    :type secret_word: str
    :param old_letters_guessed: list of letters that were already guessed by the player
    :type old_letters_guessed: list
    :return: True is the player guessed al letters in secret word or False if not
    :rtype: bool
    """
    chars = ''
    win = True
    for char in secret_word:
        if char in old_letters_guessed:
            chars = chars + char
        else:
            win = False
            break
    return win


def show_hidden_word(secret_word: str, old_letters_guessed: list) -> str:
    """
    Shows the hidden word. letters that are not guessed are replaced with "_"
    :param secret_word: The secret word chosen according to the index number
    :type secret_word: str
    :param old_letters_guessed: list of letters that were already guessed by the player
    :type old_letters_guessed: list
    :return: String built by the letters found and "_" instead of letters not yet found
    :rtype: str
    """
    guess = ''
    for char in secret_word:
        if char in old_letters_guessed:
            guess += char + " "
        else:
            guess += "_" + " "
    return guess


def check_valid_input(letter_guessed, old_letters_guessed):
    """
    checks that the input is a one English letter and also that this letter was not guessed before
    :param letter_guessed:
    :type letter_guessed: str
    :param old_letters_guessed: list of letters that were already guessed by the player
    :type old_letters_guessed: list
    :return: True or False
    :rtype: bool
    """
    if not letter_guessed.isalpha():
        return False
    letter_guessed = letter_guessed.lower()
    return len(letter_guessed) == 1 and letter_guessed not in old_letters_guessed


def try_update_letter_guessed(letter_guessed: str, old_letters_guessed: list) -> bool:
    """
    Checks if the letter is English alphabet and was not guessed already
    used the check_valid_input function
    :param letter_guessed: the letter that is guessed by the player
    :type letter_guessed: str
    :param old_letters_guessed: list of letters that were already guessed by the player
    :type old_letters_guessed: list
    :return: True or False
    :rtype: bool
    """
    if check_valid_input(letter_guessed, old_letters_guessed):
        old_letters_guessed.append(letter_guessed)
        return True
    else:
        print("X")
        print("->".join(sorted(old_letters_guessed)))
        return False


def choose_word(file_path: str, index: int) -> str:
    """
    Chooses a word from file according to the index number
    :param file_path: the location of the text file containing the words
    :type file_path: str
    :param index: the relevant index number of the word
    :type index: int
    :return: the chosen word
    :rtype: str
    """
    with open(file_path, "r", encoding='UTF8') as input_file:
        word_list = input_file.read().splitlines()
    word = word_list[index]
    return word


def main():
    # logging.basicConfig(level=logging.DEBUG)
    old_letters_guessed = []
    num_of_tries = 0
    print_logo()
    # file_path = input("Enter file path: ")
    file_path = r"""C:\python\words.txt"""
    index_word = int(input("Enter index: "))
    secret_word = choose_word(file_path, index_word)
    logging.debug(secret_word)
    print("Let's start!\n")
    print(HANGMAN_PHOTOS[num_of_tries])
    print(show_hidden_word(secret_word, old_letters_guessed) + '\n')

    while True:
        letter_guessed = input("Guess a letter: ")
        letter_valid = try_update_letter_guessed(letter_guessed, old_letters_guessed)
        logging.debug(f"old_letters_guessed :{old_letters_guessed}\n")

        # invalid input
        if not letter_valid:
            continue

        # wrong guess
        if letter_guessed not in secret_word:
            num_of_tries += 1
            print(f"{Fore.RED} :( {Style.RESET_ALL}\n")
            print(HANGMAN_PHOTOS[num_of_tries])
            print()

        print(show_hidden_word(secret_word, old_letters_guessed))

        # win game
        if check_win(secret_word, old_letters_guessed):
            print(f"{Fore.GREEN} {WINNER} {Style.RESET_ALL}\n")
            break

        # lose game
        if num_of_tries >= MAX_TRIES:
            print(f"{Fore.RED} {GAME_OVER} {Style.RESET_ALL}\n")
            break


if __name__ == '__main__':
    main()
