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