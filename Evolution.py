import random, keyboard
from Extras import Player, clear_screen, multiple_choice

# 129 total cards, 17 carnivores, 7 each for the remaining traits

def main(active_user=Player("Guest", "")):
    deck = [
        "Carnivore"] * 17 + [
        "Ambush"] * 7 + [
        "Burrowing"] * 7 + [
        "Climbing"] * 7 + [
        "Cooperation"] * 7 + [
        "Defensive Herding"] * 7 + [
        "Fat Tissue"] * 7 + [
        "Fertile"] * 7 + [
        "Foraging"] * 7 + [
        "Hard Shell"] * 7 + [
        "Horns"] * 7 + [
        "Intelligence"] * 7 + [
        "Long Neck"] * 7 + [
        "Pack Hunting"] * 7 + [
        "Scavenger"] * 7 + [
        "Symbiosis"] * 7 + [
        "Warning Call"] * 7
    playing_deck = random.shuffle(deck)
    
    print("Press 'Enter' to draw your cards.", end="", flush=True)
    event = keyboard.read_event()

if __name__ == "__main__":
    main()