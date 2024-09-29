""" Command to improve code quality """

from typing import Annotated
import typer
from huggingface_hub import InferenceClient
from rich import print
from code_pilot_cli import CHAT_LLM, SYSTEM_MESSAGE, print_highlighted


def enhance(
    code: Annotated[
        typer.FileText,
        typer.Argument(
            help="File containing code to enhance for quality improvements."
        ),
    ],
    model: Annotated[
        str,
        typer.Option(
            "--model",
            "-m",
            help="The model to run inference with. Can be a model id hosted on the "
            "Hugging Face Hub, e.g. meta-llama/Meta-Llama-3-8B-Instruct or a URL "
            "to a deployed Inference Endpoint.",
        ),
    ] = CHAT_LLM,
) -> None:
    """
    Improve code quality by applying best practices.

    Args:
        code (typer.FileText): The file containing code to be enhanced.
    """

    client = InferenceClient(model)

    try:
        response = client.chat_completion(
            messages=[
                SYSTEM_MESSAGE,
                {
                    "role": "user",
                    "content": "Apply best practices, enhancements, and industry standards to the provided "
                    f"code to make it more efficient, secure, and maintainable:\n{code.read()}",
                },
            ],
            max_tokens=2048,
        )

        print_highlighted(response.choices[0].message.content)

    except Exception as error:
        print(f"[bold red]Error[/bold red]: {error}")
