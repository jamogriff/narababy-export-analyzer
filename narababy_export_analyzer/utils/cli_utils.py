from colorama import Fore, Back, Style

def display_title(title: str):
    """Displays a yellow title with a newline for breathing room."""

    print(Fore.YELLOW + title)
    print("=" * len(title))
    print(Fore.RESET)

def display_info(message: str):
    display_right_padded_color_label("INFO", Fore.BLUE, message)

def display_success(message: str):
    display_right_padded_color_label("OK", Fore.GREEN, message)

def display_failure(message: str):
    display_right_padded_color_label("FAIL", Fore.RED, message)

def display_right_padded_color_label(label: str, colorama_fore_color: str, message: str):
    """Display a right-padded colored label and a message.

    ANSI color codes will break padding because Python counts their characters as strings.
    So we format the intended label first and then replace it with the colored version.
    """

    colored_label = "[ " + colorama_fore_color + label + Fore.RESET + " ] "
    formatted = f"{label:.<8} {message}"
    colored_output = formatted.replace(label, colored_label, 1)
    print(colored_output)

def get_elapsed_time(start: float, end: float) -> float:
    """Returns elapsed time in milliseconds."""

    return (end - start) * 1000

