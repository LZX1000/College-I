import random
from Extras import yes_or_no, clear_screen

#Input Words
def input_words():
    #Initialize words list
    words = []
    #Entering words loop
    while True:
        if len(words) > 0:
            clear_screen("Enter the words you want to guess one at a time.\nWhen you are done, type 'done'.\n" + f"{words}")
        else:
            clear_screen("Enter the words you want to guess one at a time.\nWhen you are done, type 'done'.")
        word = input("\nEnter a word: ").lower().strip()
        if word == "done":
            break
        elif any(char.isdigit() for char in word):
            print("Numbers are not allowed. Please enter a valid word.")
            continue
        elif not any(char.isalpha() for char in word):
            print("You need at least one letter. Please enter a valid word.")
        elif any(char == '_' for char in word):
            print("Underscores are not currently supported. Please enter a valid word.")
        words.append(word)
        #Sort words alphabetically
        words.sort()
    #Check if words[] is empty
    if len(words) == 0:
        print("You must enter at least one word.")
        return input_words()
    #Return words
    return words

#Get Random Word
def get_word(words=None):
    #Check paramaters
    if words == None:
        words = input_words()
    #Chooses a random word from words[] list
    random_word = random.choice(words)
    #Returns a random word
    return random_word 

#Try Again
def try_again(guessed_letters=None, guesses=0, words=None):
    #Check parameters
    if words is None:
        words = input_words()
    if guessed_letters is None:
        guessed_letters = []
    #Ask if the player wants to play again
    if guesses == len(guessed_letters) or guesses < len(guessed_letters):
        print("*Perfect!*\n")
    print(f"Congrats! You guessed it in {guesses} guesses. Try again? (Y/N)\n")
    response = yes_or_no()
    #If the player wants to play again
    if response == "y":
        clear_screen()
        #Checks if the player wants new words
        print("Would you like to use the same words? (Y/N)\n")
        same_words = yes_or_no()
        clear_screen()
        if same_words == "y":
            main(words=words)
        elif same_words == "n":
            main(words=None)
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
def main(game_word=None, guesses=0, game_letters=None, guessed_letters=None, words=None, missed_letters=None):
    clear_screen()
    #Check parameters
    if words is None:
        words = input_words()
    if game_word is None:
        game_word = get_word(words=words)
    if game_letters is None:
        game_letters = list(game_word)
    if guessed_letters is None:
        guessed_letters = ['_' if letter.isalpha() else letter for letter in game_letters]
    if missed_letters is None:
        missed_letters = []
    display_game = f"Word: " + " ".join(guessed_letters) + "\nMissed Letters: " + ", ".join(missed_letters) + f"\nGuesses: {guesses}\n"
    #Print the game screen
    clear_screen()
    print(f"Word: " + " ".join(guessed_letters) + "\nMissed Letters: " + ", ".join(missed_letters) + f"\nGuesses: {guesses}\n")
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
        #Guess is not in the word
        else:
            #Guess hasn't been guessed before
            if guess not in missed_letters:
                missed_letters.append(guess)
            guesses += 1
        return main(game_word, guesses, game_letters, guessed_letters, words, missed_letters)    
    #Display game results and ask if the player wants to play again    
    else:
        clear_screen()
        print(f"Word: " + " ".join(guessed_letters) + "\nMissed Letters: " + ", ".join(missed_letters) + f"\nGuesses: {guesses}\n")
        response = try_again(guessed_letters=guessed_letters, guesses=guesses, words=words)
        #Quit game
        if response == "n":
            return

if __name__ == "__main__":
    response = main()