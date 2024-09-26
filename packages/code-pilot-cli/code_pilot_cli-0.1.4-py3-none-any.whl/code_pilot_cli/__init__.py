"""
CodePilot CLI: Your customizable coding assistant for the command line interface (CLI).
"""

from rich.console import Console
from rich.syntax import Syntax


# Constants
CHAT_LLM = "HuggingFaceH4/starchat2-15b-v0.1"
COMPLETION_LLM = "bigcode/starcoder2-15b"
SYSTEM_MESSAGE = {
    "role": "system",
    "content": "You are CodePilot, an advanced coding assistant powered by "
    "state-of-the-art Large Language Models, and specifically optimized for enhanced "
    "performance in coding tasks.",
}


# Syntax Highlighting
def print_highlighted(code: str) -> None:
    """
    Highlight and print the provided code.

    Args:
        code (str): The code to be highlighted and printed.
    """

    console = Console()
    highlighted_code = Syntax(
        code,
        "markdown",
        theme="github-dark",
        code_width=120,
        word_wrap=True,
        background_color="default",
    )

    console.print(highlighted_code)
