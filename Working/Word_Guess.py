#Imports
import random
from Extras import yes_or_no, clear_screen

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
def get_word(words=None):
    if words == None:
        words = input_words()

    random_word = random.choice(words)

    return random_word 

#Try Again
def try_again(guesses=0, words=None):
    if words is None:
        words = input_words()
    if guesses == 0:
        main(words=words)

    print(f"Congrats! You guessed it in {guesses} guesses. Try again? (Y/N)\n")
    
    response = yes_or_no()
    if response == "y":
        clear_screen()

        print("Would you like to use the same words? (Y/N)\n")
        
        same_words = yes_or_no()
        clear_screen()

        if same_words == "y":
            main(words=words)

        elif same_words == "n":
            main(words=None)

    elif response == "n":
        exit()

#Check Guess
def check_guess():
    guess = input("Guess a letter: ").lower()
    
    if len(guess) == 1:
        if any(char.isdigit() for char in guess):
            print("Numbers are not allowed. Please enter a single letter.\n")
            return check_guess()

        else:
            return guess
    
    else:
        print("Please enter a single letter.\n")
        return check_guess()
        
#Guessing
def main(game_word=None, guesses=0, game_letters=None, guessed_letters=None, words=None, missed_letters=None):
    clear_screen()

    if words is None:
        words = input_words()
    if game_word is None:
        game_word = get_word(words)
    if game_letters is None:
        game_letters = list(game_word)
    if guessed_letters is None:
        guessed_letters = ['_' for _ in game_letters]
    if missed_letters is None:
        missed_letters = []

    clear_screen()
    print(f"Word: " + " ".join(guessed_letters) + "\nMissed Letters: " + ", ".join(missed_letters) + f"\nGuesses: {guesses}\n")

    if "_" in guessed_letters: 
        guess = check_guess()
        
        if guess not in guessed_letters and guess not in missed_letters:
            if guess in game_letters:
                for i, letter in enumerate(game_letters):
                    if guess == letter:
                        guessed_letters[i] = letter
                guesses += 1
            else:
                if guess not in missed_letters:
                    missed_letters.append(guess)
                    guesses += 1
        else:
            print("You already guessed that letter. Try again.\n")
        return main(game_word, guesses, game_letters, guessed_letters, words, missed_letters)        
    else:
        clear_screen()
        print(f"Word: " + " ".join(guessed_letters) + "\nMissed Letters: " + ", ".join(missed_letters) + f"\nGuesses: {guesses}\n")
        try_again(guesses, words)

if __name__ == "__main__":
    main()