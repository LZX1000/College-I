import os
import keyboard
from typing import overload, Union, List

class Player:
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password

    def __str__(self) -> str:
        return f"{self.username}, {self.password}"

def exception_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"An error occurred: {e}")
    return wrapper

def clear_screen(prompt: str | None) -> None:
    os.system('cls' if os.name == 'nt' else 'clear')
    if prompt: print(prompt)

@exception_handler
def clear_input() -> None:
    keyboard.send('enter')
    input()

@overload
def handle_value(
    prompt: str | None = " ",
    style: Union[int, float] = 0
) -> Union[int, float]: ...

@overload
def handle_value(
    prompt: str | None = " ",
    style: str | None = " ",
    name: str | None = "string"
) -> str: ...

def handle_value(
    prompt: str | None = " ",
    style: Union[int, float, str] | None = 0,
    name: str | None = "string"
) -> Union[int, float, str]:
    while True:
        try:
            user_input = input(prompt)
            if isinstance(style, int):
                return int(user_input)
            elif isinstance(style, float):
                return float(user_input)
            elif isinstance(style, str):
                user_input = user_input.strip()
                if user_input:
                    if style == " ":
                        return user_input
                    elif style == "_":
                        return user_input.replace(" ", "_")
        except ValueError:
            clear_screen(f"Please enter a valid {name if isinstance(style, str) else "number"}.\n")

@exception_handler
def yes_or_no(prompt: str | None = " ") -> str:
    while True:
        print(prompt)
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            if event.name in ["n", "0"]:
                clear_input()
                return "n"
            elif event.name in ["y", "1"]:
                clear_input()
                return "y"
        clear_screen('Please enter "Y" or "N".\n')

@exception_handler
def check_menu_choice(menu: List[str], prompt: str | None = " ") -> str:
    while True:
        print(prompt)
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            try:
                if int(event.name) in range(len(menu)):
                    clear_input()
                    return menu[int(event.name)]
            except ValueError:
                choice = input()
                if choice.strip().lower().replace(" ", "_") in [item.strip().lower().replace(" ", "_") for item in menu]:
                    return choice
        clear_screen() if event.name == "enter" else clear_screen("Invalid choice.\n")

def main() -> None:
    pass

if __name__ == "__main__":
    main()