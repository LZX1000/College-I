import os
import keyboard
from functools import singledispatch
from typing import Union

class Player:
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password

    def __str__(self) -> str:
        return f"{self.username}, {self.password}"

def clear_screen(prompt: str | None) -> None:
    os.system('cls' if os.name == 'nt' else 'clear')
    if prompt:
        print(prompt)

@singledispatch
def handle_input(prompt: str | None) -> None:
    raise NotImplementedError("Unsupported type")

@handle_input.register
def _(
    prompt: str | None = " ",
    style: Union[int, float] = 0
    ) -> Union[int, float]:
    while True:
        try:
            user_input = input(prompt)
            if isinstance(style, int):
                return int(user_input)
            elif isinstance(style, float):
                return float(user_input)
        except ValueError:
            clear_screen("Please enter a valid number.\n")

@handle_input.register
def _(
    prompt: str | None = " ",
    style: str | None = " ",
    name: str | None = "string"
    ) -> str:
    while True:
        user_input = input(prompt).strip()
        if user_input:
            if style == " ":
                return user_input
            elif style == "_":
                return user_input.replace(" ", "_")
        clear_screen(f"Please enter a valid {name}.\n")

def clear_input() -> None:
    keyboard.send('enter')
    input()

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
        else:
            clear_screen('Please enter "Y" or "N".\n')

def check_menu_choice(
    menu: list[str],
    prompt: str | None = " "
    ) -> str:
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