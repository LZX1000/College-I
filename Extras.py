import os, keyboard, time

def yes_or_no(prompt=""):
    while True:
        response = input(prompt).strip().lower()
        if response in ["y", "yes", "1"]:
            return "y"
        elif response in ["n", "no", "0"]:
            return "n"
        else:
            clear_screen('Please enter "Y" or "N".\n')

def clear_screen(prompt=""):
    os.system('cls' if os.name == 'nt' else 'clear')
    if prompt != "":
        print(prompt)

def handle_value_error(prompt=""):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            clear_screen("Please enter a valid integer.\n")

def sleepy(seconds, key=None):
    for i in range(int(seconds)*20):
        time.sleep(0.05)
        if keyboard.is_pressed('w') or keyboard.is_pressed('up'):
            key = "w"
        elif keyboard.is_pressed('s') or keyboard.is_pressed('down'):
            key = "s"
        elif keyboard.is_pressed('a') or keyboard.is_pressed('left'):
            key = "a"
        elif keyboard.is_pressed('d') or keyboard.is_pressed('right'):
            key = "d"
    return key

def main():
    print("I am but a humble module file.")

if __name__ == "__main__":
    main()