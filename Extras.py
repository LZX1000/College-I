import os
import time
import keyboard
from typing import overload, Union, List, Set

class Player:
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password

    def __str__(self) -> str:
        return f"{self.username}, {self.password}"

def clear_screen(
    prompt: str | None = None, /, 
    flush: bool | None = False
) -> None:
    os.system('cls' if os.name == 'nt' else 'clear')
    if prompt:
        print(prompt, flush=flush)

def f_input(
    prompt: str | None = " ", /,
    end: str = "",
    flush: bool | None = False,
) -> str:
    print(prompt, end=end, flush=flush)
    return input()

@overload
def handle_value(
    prompt: str | None = " ",
    style: Union[int, float] = 0,
    name: str | None = "number"
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
    name: str | None = "input"
) -> Union[int, float, str]:
    if name == "input" and isinstance(style, int or float):
        name = "number"
    elif name == "input" and isinstance(style, str):
        name = "string"

    while True:
        user_input = f_input(prompt, flush=True)
        if user_input:
            if isinstance(style, int):
                if user_input.isdigit():
                    return int(user_input)
                else:
                    clear_screen(f"Please enter a valid integer.\n")
            elif isinstance(style, float):
                try:
                    return float(user_input)
                except ValueError:
                    clear_screen(f"Please enter a valid float.\n")
            elif isinstance(style, str):
                    if style == " ":
                        return user_input.strip()
                    elif style == "_":
                        return user_input.strip().replace(" ", "_")
        else:
            clear_screen(f"Please enter a valid {name}.\n")

def multiple_choice(
    prompt: str | None = " ",
    options: Union[List[str], Set[str]] | None = {"Yes", "No"},
    active_option: int | None = 0,
    end: str = "\n\n"
) -> str:
    def render() -> None:
        print(prompt, end=end)
        for i, option in enumerate(options):
            if i == active_option:
                print(f"\033[30;47m{option}\033[0m")
            else:
                print(option)

    print("\033[?25l", end="", flush=True)
    clear_screen()
    render()

    options = list(options)
    while True:
        event = keyboard.read_event()
        old_active_option = active_option
        if event.event_type == keyboard.KEY_DOWN:
            if event.name in {"up", "w"}:
                active_option = (active_option - 1) % len(options)
            elif event.name in {"down", "s"}:
                active_option = (active_option + 1) % len(options)
            elif event.name in {"enter", "space"}:
                print("\033[?25h", end="", flush=True)
                f_input(end="")
                if set(options) == {"Yes", "No"}:
                    return options[active_option].lower()[0]
                else:
                    return options[active_option].lower().replace(" ", "_")
            if active_option != old_active_option:
                clear_screen()
                render()

def main() -> None:
    pass

if __name__ == "__main__":
    main()