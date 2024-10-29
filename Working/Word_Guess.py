import random
from Extras import yes_or_no, clear_screen

#Input Words
def input_words(words=None):
    if words is None:
        words = []
    #Entering words loop
    while True:
        if len(words) > 0:
            print("Enter the words you want to guess one at a time.\nWhen you are done, type 'done'.\n" + f"{words}")
        else:
            print("Enter the words you want to guess one at a time.\nWhen you are done, type 'done'.")
        word = input("\nEnter a word: ").lower().strip()
        if word == "done":
            if len(words) == 0:
                clear_screen("You must enter at least one word.\n")
            else:
                break
        elif any(char.isdigit() for char in word):
            clear_screen("Numbers are not allowed. Please enter a valid word.\n")
        elif not any(char.isalpha() for char in word):
            clear_screen("You need at least one letter. Please enter a valid word.\n")
        elif any(char == '_' for char in word):
            clear_screen("Underscores are not currently supported. Please enter another word.\n")
        elif word in words:
            clear_screen("You already entered that word. Please enter a new word.\n")
        else:
            words.append(word)
            clear_screen()
        #Sort words alphabetically
        words.sort()
    #Chooses a random word from words[] list
    game_word = random.choice(words)
    #Returns a random word
    perfect_word = ''.join(sorted(set(char for char in game_word if char.isalpha())))
    return game_word, perfect_word, words

#Try Again
def try_again(guesses=0, words=None, perfect_word=None):
    #Check parameters
    if words is None:
        words = input_words()
    #Ask if the player wants to play again
    if guesses == len(perfect_word):
        print("*Perfect!*\n")
    response = yes_or_no(f"Congrats! You guessed it in {guesses} guesses. Try again? (Y/N)\n")
    #If the player wants to play again
    if response == "y":
        #Checks if the player wants new words
        clear_screen("Would you like to use the same words? (Y/N)\n")
        same_words = yes_or_no()
        clear_screen()
        if same_words == "y":
            return words
        elif same_words == "n":
            return None
    #Returns if the player doesn't want to play again
    elif response == "n":
        return response

#Check Guess
def check_guess(display_game="",guessed_letters=None, missed_letters=None, guesses=0):
    #Check parameters
    if guessed_letters is None:
        guessed_letters = []
    if missed_letters is None:
        missed_letters = []
    while True:
        guess = input("Guess a letter: ").lower()
        #Check if the guess is a single letter
        if len(guess) == 1 and guess.isalpha():
            #Check if the guess is a letter
            if any(char.isdigit() for char in guess):
                clear_screen(display_game + "\nNumbers are not allowed. Please enter a single letter.\n")
            #Check if the guess has already been guessed
            elif guess in guessed_letters or guess in missed_letters:
                clear_screen(display_game + "\nYou already guessed that letter. Try again.\n")
            #Return the proper guess
            else:
                return guess
        #Ask for a new, single-letter guess
        elif len(guess) > 1:
            clear_screen(display_game + "\nPlease enter a single letter.\n")
        #Ask for a new, letter guess
        elif not guess.isalpha():
            clear_screen(display_game + "\nPlease enter a letter.\n")
        #Ask for a new guess because the guess was just weird
        else:
            clear_screen(display_game + "\nPlease enter a valid letter.\n")
        
#Guessing
def main(game_word=None, guesses=0, game_letters=None, guessed_letters=None, words=None, missed_letters=None, perfect_word=None):
    while True:
        clear_screen()
        #Check parameters
        if words is None:
            game_word, perfect_word, words = input_words()
        if game_word is None or perfect_word is None:
            game_word, perfect_word = input_words(words=words)
        if game_letters is None:
            game_letters = list(game_word)
        if guessed_letters is None:
            guessed_letters = ['_' if letter.isalpha() else letter for letter in game_letters]
        if missed_letters is None:
            missed_letters = []
        display_game = f"Word: " + " ".join(guessed_letters) + "\nMissed Letters: " + ", ".join(missed_letters) + f"\nGuesses: {guesses}\n"
        clear_screen(display_game)
        #Check if there are characters left to guess
        if "_" in guessed_letters:
            #Get a proper guess 
            guess = check_guess(display_game=display_game, guessed_letters=guessed_letters, missed_letters=missed_letters, guesses=guesses)
            #Check if the guess is in the word
            if guess in game_letters:
                for i, letter in enumerate(game_letters):
                    if guess == letter:
                        guessed_letters[i] = letter
                guesses += 1
            else:
                #Guess hasn't been guessed before
                if guess not in missed_letters:
                    missed_letters.append(guess)
                guesses += 1
        #Display game results and ask if the player wants to play again    
        else:
            clear_screen(display_game)
            response = try_again(guesses=guesses, words=words, perfect_word=perfect_word)
            if response is None:
                words = None
            #Quit game
            if response == "n":
                return
            game_word, perfect_word, words = input_words(words=words)
            game_letters = list(game_word)
            guessed_letters = ['_' if letter.isalpha() else letter for letter in game_letters]
            missed_letters = []
            guesses = 0

if __name__ == "__main__":
    response = main()