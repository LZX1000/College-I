#Imports

import random

#Clear Screen

def clear_screen():
    print("\n" * 50)

#Input Words

def input_words():
    print("Enter the words you want to guess one at a time.\nWhen you are done, type 'done'.")
    words = []
    while True:
        word = input("Enter a word: ").lower()
        if word == "done":
            break
        elif any(char.isdigit() for char in words):
            print("Numbers are not allowed. Please enter a valid word.")
            continue
        words.append(word)

    return words

#Get Word

def get_word():
    random_word = random.choice(WORDS)

    return random_word 

#Try Again

def try_again():
    print(f"Congrats! You guessed it in {GUESSES} guesses. Try again? (Y/N)\n")
    
    response = yes_or_no()
    if response == "y":
        print("Would you like to use the same words? (Y/N)\n")
        
        same_words = yes_or_no()
        clear_screen()

        if same_words == "y":
            game()

        elif same_words == "n":
            main()

    elif response == "n":
        exit()

#Yes or No

def yes_or_no():
    while True:
        response = input().lower()

        if response == "y":
            return response
        elif response == "n":
            return response
        else:
            print('\nPlease enter "Y" or "N".\n')

#Game Loop

def game():
    global GUESSES

    game_word = get_word()
    game_letters = list(game_word)
    guessed_letters = ['_' for _ in game_letters]
    GUESSES = 0

    while True:
        for i, game_letter in enumerate(game_letters):
            if guessed_letters[i] != "_":
                print(game_letter, end="")
            elif game_letter.islower():
                print("_", end="")
        print("\n")

        guess = input("Guess a letter: ").lower()

        for i, game_letter in enumerate(game_letters):
            if guess == game_letter:
                guessed_letters[i] = game_letter
            else:
                continue

        if "_" not in guessed_letters:
            GUESSES += 1
            try_again()

        else:
            GUESSES += 1
            continue

#main loop

def main():
    global WORDS

    WORDS = input_words()
    game()

if __name__ == "__main__":
    main()