import colorama
from colorama import Back, Fore, Style

colorama.init(autoreset=True)


def style_text(text, color=Fore.WHITE, background=Back.RESET, style=Style.NORMAL):
    return color + text + background + style + Fore.RESET


def style_text_multicolor(text, style=Style.BRIGHT):
    colors = [
        Fore.RED,
        Fore.GREEN,
        Fore.YELLOW,
        Fore.BLUE,
        Fore.MAGENTA,
        Fore.CYAN,
        Fore.WHITE,
    ]
    new_text = ""
    for letter in text:
        for color in colors:
            new_text = new_text + f"{color + letter}"
            move_color = colors.pop(0)
            colors.append(move_color)
            break
    print(style + new_text + Style.BRIGHT)
