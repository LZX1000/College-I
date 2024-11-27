from random import choice
from Extras import yes_or_no, clear_screen

def input_words(words, parameter=0):
    if parameter == 0:
        words = []
        #Entering words loop
        while True:
            if len(words) > 0:
                print("Enter the words/phrases you want to guess one at a time.\nWhen you are done, type 'done'.\n" + f"[{', '.join(word for word, _ in words)}]")
            else:
                print("Enter the words/phrases you want to guess one at a time.\nWhen you are done, type 'done'.")
            word = input("\nEnter a word or phrase: ").lower().strip()
            if word == "done":
                if len(words) == 0:
                    clear_screen("You must enter at least one word or phrase.\n")
                else:
                    break
            elif any(char.isdigit() for char in word):
                clear_screen("Numbers are not allowed. Please enter a valid word or phrase.\n")
            elif not any(char.isalpha() for char in word):
                clear_screen("You need at least one letter. Please enter a valid word or phrase.\n")
            elif word in words:
                clear_screen("You already entered that word/phrase. Please enter a new word or phrase.\n")
            else:
                words.append((word, "Phrase") if " " in word else (word, "Word"))
                clear_screen()
            words.sort()
            #Add words to the words file
            try:
                with open("words.txt", "r") as file:
                    old_words = [line for line in file.readlines()]
                    for word, option in words:
                        if (word, option) not in (old_words[0], old_words[1]):
                            perfect_word = ''.join(sorted(set(char for char in word if char.isalpha())))
                            with open("words.txt", "a") as file:
                                file.write(f"{word}, {option}, {perfect_word}\n")
            except FileNotFoundError:
                with open("words.txt", "w") as file:
                    for word, option in words:
                        perfect_word = ''.join(sorted(set(char for char in word if char.isalpha())))
                        file.write(f"{word}, {option}, {perfect_word}\n")
    #Chooses a random word from words[] list
    game_word = choice(words)
    game_word = (game_word[0], game_word[1], ''.join(sorted(set(char for char in game_word[0] if char.isalpha()))))
    return game_word, words

def main(active_user='guest, None'):
    words = None
    game_word = None
    while True:
        clear_screen()
        if not words:
            response = yes_or_no("Would you like to use random words? (Y/N)\n\n")
            if response == "n":
                clear_screen()
                game_word, words = input_words()
            # Open existing words file or create a new one
            elif response == "y":
                try:
                    with open("words.txt", "r") as file:
                        words = [tuple(line.strip().split(', ')) for line in file.readlines()]
                except FileNotFoundError:
                    clear_screen("No words found. Please enter some words.\n")
                    game_word, words = input_words()
                (game_word, option, perfect_word), words = input_words(words, parameter=1)
        else:
            game_word, option, perfect_word = input_words(words, parameter=1)
        game_letters = list(game_word)
        guessed_letters = ['ab' if letter.isalpha() else letter for letter in game_letters]
        missed_letters = []
        guesses = 0
        while True:
            # Display game
            display_game = f"{option}: " + " ".join('_' if letter == "ab" else letter for letter in guessed_letters) + "\nMissed Letters: " + ", ".join(missed_letters) + f"\nGuesses: {guesses}\n"
            clear_screen(display_game)
            # Get a guess if there are characters left to guess
            if "ab" in guessed_letters:
                while True:
                    guess = input("Guess a letter: ").lower()
                    # Check guess
                    if len(guess) == 1 and guess.isalpha():
                        if any(char.isdigit() for char in guess):
                            clear_screen(display_game + "\nNumbers are not allowed. Please enter a single letter.\n")
                        elif guess in guessed_letters or guess in missed_letters:
                            clear_screen(display_game + "\nYou already guessed that letter. Try again.\n")
                        else:
                            break
                    # Error messages
                    elif len(guess) > 1:
                        clear_screen(display_game + "\nPlease enter a single letter.\n")
                    elif not guess.isalpha():
                        clear_screen(display_game + "\nPlease enter a letter.\n")
                    else:
                        clear_screen(display_game + "\nPlease enter a valid letter.\n")
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
                if guesses == len(perfect_word):
                    print("*Perfect!*\n")
                response = yes_or_no(f"Congrats! You guessed {game_word} in {guesses} guesses. Try again? (Y/N)\n\n")
                # Player plays again
                if response == "y":
                    clear_screen()
                    same_words = yes_or_no("Would you like to use the same words/phrases? (Y/N)\n\n")
                    clear_screen()
                    if same_words == "n":
                        words = None
                    break
                # Quit game
                if response == "n":
                    return 'Word Guess', active_user, None

if __name__ == "__main__":
    response = main()