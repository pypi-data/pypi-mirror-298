import random
from words import words
import string
from colorama import Fore, Back, Style
from datetime import datetime, timedelta

# the reward for winning, lottery numbers
randList, run = [], 0
while run < 6:
    number = random.randint(1, 51)
    if number not in randList:
        if run == 5:
            randList.append("+" + str(number))
            break
        randList.append(number)
        run += 1

today = datetime.today()
name = input("What is your name?")

print("-" * 50)

# explanation and rules
print(
    f"{Fore.CYAN}{Back.MAGENTA}{Style.BRIGHT}This is a game of hangman, every false guess will built the scaffold, after 6 incorrect guesses the scaffold will be finished and you will be hanged"
)
print(f"{Style.RESET_ALL}")

print("-" * 50)

print(f"{Fore.BLUE}So good luck " + name, ",try not to get hanged")
print(f"{Style.RESET_ALL}")

print("-" * 50)

print("you begin at,")
print(today)

# chosing a random word to guess
def get_valid_word(words):
    word = random.choice(words)
    while "-" in word or " " in word:
        word = random.choice(words)
    return word.upper()


# defining the game
def hangman():
    word = get_valid_word(words)
    word_letters = set(word)
    # breaks the full words into letters
    alphabet = set(string.ascii_uppercase)
    used_letters = set()

    lives = 6

    # keeping track of used letters
    while len(word_letters) > 0 and lives > 0:
        print(
            "You have",
            lives,
            "lives left and these are used letters ",
            " ".join(used_letters),
        )

        # the current word
        word_list = [letter if letter in used_letters else "_" for letter in word]
        print("Word: ", " ".join(word_list))

        user_letter = input("Guess a letter: ").upper()
        if user_letter in alphabet - used_letters:
            used_letters.add(user_letter)
            if user_letter in word_letters:
                word_letters.remove(user_letter)
            else:
                lives = lives - 1
                print(f"{Fore.RED}letter is not in word")
                print(f"{Style.RESET_ALL}")
        elif user_letter in used_letters:
            print(f"{Fore.YELLOW}(You have already used that letter")
            print(f"{Style.RESET_ALL}")
        else:
            print("Invalid character")
            print(f"{Style.RESET_ALL}")
    # if you lose
    if lives == 0:
        print(
            f"{Fore.WHITE}{Back.RED}{Style.BRIGHT}You have lost, The word was, " + word
        )
        print("you got hanged at")
        print(today)
        print(f"{Style.RESET_ALL}")
        print(f"{Style.RESET_ALL}")
    # if you win
    else:
        print(f"{Fore.RED}{Back.YELLOW}{Style.BRIGHT} You have guessed correcly")
        print("As a reward you get get the winning lottery numbers")
        print(randList)
        print(" They will definetly win, but I do not know when")
        print(f"{Style.RESET_ALL}")


hangman()
