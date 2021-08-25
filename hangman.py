import random

HANGMAN_PHOTOS = {
    1:  r"""x-------x""",
    2:  r"""x-------x
|
|
|
|
|""",
    3:  r"""x-------x
|       |
|       0
|
|
|""",
    4:  r"""x-------x
|       |
|       0
|       |
|
|""",
    5:  r"""x-------x
|       |
|       0
|      /|\
|
|""",
    6:  r"""x-------x
|       |
|       0
|      /|\
|      /
|""",
    7:  r"""x-------x
|       |
|       0
|      /|\
|      / \
|"""
                  }


def suggest_random_word(content: list) -> str:
    pick_random_word = content[random.randint(0, 6)]
    return pick_random_word


def print_hangman(num_of_tries: int) -> None:
    """Print current hangman photo.

    :param num_of_tries: num of the photo to print.
    :type num_of_tries: int
    :return: None.
    """
    print(HANGMAN_PHOTOS[num_of_tries])


def show_hidden_word(secret_word, old_letters_guessed):
    guess = ''
    for char in secret_word:
        if char in old_letters_guessed:
            guess = guess + char + " "
        else:
            guess = guess + "_" + " "
    return guess


def main():
    tries = 1
    guessed_letters = []
    letters_guessed = []

    with open(r"C:\python\words.txt", "r", encoding='UTF8') as input_file:
        word_list = input_file.read().splitlines()

    random_word = suggest_random_word(word_list)

    while True:
        print(f"random_word: {random_word}")
        print(show_hidden_word(random_word, letters_guessed))
        user_choice = input("Please type your guess letter: ").lower()

        if len(user_choice) > 1:
            print("\n\n### You entered more than one letter. Game Over! ###")
            break

        guessed_letters.append(user_choice)

        for letter in user_choice:
            if letter in random_word and letter not in letters_guessed:
                letters_guessed.append(letter)
            elif letter not in letters_guessed:
                tries += 1
            else:
                pass

        print(f"letters guessed: {letters_guessed}")

        # dict used to remove duplicates
        if sorted(list(dict.fromkeys(random_word))) == sorted(letters_guessed):
            print("\n\n---### W I N N E R ###---\n\n")
            print(show_hidden_word(random_word, letters_guessed))
            break
        elif tries == 7:
            print_hangman(tries)
            print("\n##### GAME OVER #####\n")
            break
        else:
            print_hangman(tries)


if __name__ == '__main__':
    main()
