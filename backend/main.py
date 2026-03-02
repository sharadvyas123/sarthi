# import time
# import sys
# import os
# os.environ["TRANSFORMERS_VERBOSITY"] = "error"
# os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"

# from rich.console import Console
# from rich.panel import Panel
# from rich.align import Align
# from rich.text import Text
# from rich.prompt import Prompt

# import pyfiglet

# from app.agent.graph import agent
# from app.agent.state import SarthiState

# console = Console()


# def print_banner():
#     ascii_art = pyfiglet.figlet_format("SARTHI", font="big")
#     panel = Panel(
#         Align.center(
#             Text.assemble(
#                 Text(ascii_art, style="bold yellow"),
#                 Text("\n"),
#                 Text("🪷  Geeta RAG — Your Divine Guide  🪷", style="bold yellow"),
#             )
#         ),
#         border_style="bright_magenta",
#         padding=(1, 4),
#     )
#     console.print(panel)


# def get_answer(question):
#     initial_state = SarthiState(question=question)
#     final_state = agent.invoke(initial_state)
#     return final_state["answer"]


# def typewriter(text, speed=0.02):
#     for char in text:
#         sys.stdout.write(char)
#         sys.stdout.flush()
#         time.sleep(speed)
#     print()


# def print_krishna_message(answer):
#     # Print the panel border/title first
#     console.print(Panel(
#         "",
#         title="[bold yellow]🪷 Sarthi speaks[/bold yellow]",
#         border_style="bright_blue",
#         padding=(0, 2)
#     ))
#     # Then typewriter the answer below it
#     console.print()
#     sys.stdout.write("  ")
#     typewriter(answer, speed=0.02)
#     console.print()


# def farewell():
#     message = (
#         "\nGo forth, dear one.\n\n"
#         "The answers you seek were always within you.\n"
#         "I merely helped you hear them.\n\n"
#         "Walk in dharma. Walk without fear.\n\n"
#         "        — Sarthi 🪷\n"
#     )
#     panel = Panel(
#         Align.center(Text(message, style="italic yellow")),
#         title="[bold magenta]🙏 Farewell[/bold magenta]",
#         border_style="bright_magenta",
#         padding=(1, 4),
#     )
#     console.print(panel)


# def main():
#     print_banner()
#     console.print("\n[dim]Type 'quit' to exit[/dim]\n")

#     while True:
#         question = Prompt.ask("[bold green]🧘 Ask Sarthi[/bold green]")

#         if question.lower() in ["quit", "exit"]:
#             farewell()
#             break

#         if not question.strip():
#             continue

#         console.print("\n[cyan]⏳ Consulting the eternal wisdom of the Gita...[/cyan]\n")

#         answer = get_answer(question)

#         print_krishna_message(answer)


# if __name__ == "__main__":
#     main()




import time
import sys
import os

os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"

from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich.prompt import Prompt
from rich.live import Live
from rich.box import ROUNDED

import pyfiglet

from app.agent.graph import agent
from app.agent.state import SarthiState


console = Console()


# Warm divine color palette
GOLD = "#FFD700"
SAFFRON = "#FF9933"
LOTUS = "#FF6F61"
CREAM = "#FFF5E1"
SUNRISE = "#FFA500"


# -------------------------
# Banner
# -------------------------
def print_banner():

    ascii_art = pyfiglet.figlet_format("SARTHII", font="slant")

    title = Text(ascii_art, style=f"bold {GOLD}")

    subtitle = Text(
        "🪷 Geeta RAG — Your Divine Guide 🪷",
        style=f"bold {SAFFRON}"
    )

    divider = Text(
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        style=SUNRISE
    )

    content = Align.center(title + "\n" + divider + "\n" + subtitle)

    panel = Panel(
        content,
        border_style=SAFFRON,
        box=ROUNDED,
        padding=(1, 4),
    )

    console.print(panel)


# -------------------------
# Get answer from agent
# -------------------------
def get_answer(question):

    initial_state = SarthiState(question=question)
    final_state = agent.invoke(initial_state)

    return final_state["answer"]


# -------------------------
# Typewriter inside panel
# -------------------------
def typewriter_panel(answer):

    displayed = ""

    panel = Panel(
        Text(displayed, style=CREAM),
        title=f"[bold {GOLD}]🪷 Sarthii speaks[/bold {GOLD}]",
        border_style=LOTUS,
        box=ROUNDED,
        padding=(1, 2),
    )

    with Live(panel, console=console, refresh_per_second=30) as live:

        for char in answer:

            displayed += char

            panel = Panel(
                Text(displayed, style=CREAM),
                title=f"[bold {GOLD}]🪷 Sarthii speaks[/bold {GOLD}]",
                border_style=LOTUS,
                box=ROUNDED,
                padding=(1, 2),
            )

            live.update(panel)

            time.sleep(0.01)


# -------------------------
# Farewell
# -------------------------
def farewell():

    message = (
        "\nGo forth, dear one.\n\n"
        "The light you seek is already within you.\n\n"
        "Whenever confusion arises,\n"
        "return... and I shall guide you.\n\n"
        "        — Sarthii 🪷\n"
    )

    panel = Panel(
        Align.center(Text(message, style=CREAM)),
        title=f"[bold {GOLD}]🙏 Farewell[/bold {GOLD}]",
        border_style=SAFFRON,
        box=ROUNDED,
        padding=(1, 4),
    )

    console.print(panel)


# -------------------------
# Main loop
# -------------------------
def main():

    print_banner()

    console.print(
        f"\n[bold {SUNRISE}]✨ I am Sarthii. Ask, and I shall guide you.[/bold {SUNRISE}]\n"
    )

    console.print("[dim]Type 'quit' to exit[/dim]\n")

    while True:

        question = Prompt.ask(
            f"[bold {SAFFRON}]🧘 Ask Sarthii[/bold {SAFFRON}]"
        )

        if question.lower() in ["quit", "exit"]:

            farewell()
            break

        if not question.strip():
            continue

        console.print(
            f"\n[bold {SUNRISE}]⏳ Consulting the eternal wisdom...[/bold {SUNRISE}]\n"
        )

        answer = get_answer(question)

        typewriter_panel(answer)


# -------------------------
if __name__ == "__main__":
    main()