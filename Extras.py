import os
import keyboard
from typing import overload, Union, List

class Player:
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password

    def __str__(self) -> str:
        return f"{self.username}, {self.password}"

def clear_screen(prompt: str | None = None) -> None:
    os.system('cls' if os.name == 'nt' else 'clear')
    if prompt:
        print(prompt)

def clear_input(keys: List[str] = "enter") -> None:
    while any(keyboard.is_pressed(key) for key in keys):
        keyboard.read_event(suppress=True)

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
        clear_input()
        user_input = input(prompt)
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
        clear_screen(f"Please enter a valid {name}.\n")

def multiple_choice(
    prompt: str | None = " ",
    options: List[str] | None = ["Yes", "No"],
    end: str = "\n\n",
    active_option: int | None = 0
) -> str:
    def render() -> None:
        print(prompt, end=end)
        for i, option in enumerate(options):
            if i == active_option:
                print(f"\033[30;47m{option}\033[0m")
            else:
                print(option)

    options = [str(option) for option in options]

    print("\033[?25l", end="")
    clear_screen()
    render()

    clear_input()
    while True:
        event = keyboard.read_event()
        old_active_option = active_option
        if event.event_type == keyboard.KEY_DOWN:
            if event.name in ["up", "w"]:
                active_option = (active_option - 1) % len(options)
            elif event.name in ["down", "s"]:
                active_option = (active_option + 1) % len(options)
            elif event.name in ["enter", "space"]:
                clear_input()
                print("\033[?25h", end="", flush=True)
                if options == ["Yes", "No"]:
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