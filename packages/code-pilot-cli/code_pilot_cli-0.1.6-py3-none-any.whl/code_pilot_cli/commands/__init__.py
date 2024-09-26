""" CodePilot commands """

from code_pilot_cli.commands.ai import ai
from code_pilot_cli.commands.chat import chat
from code_pilot_cli.commands.completions import completions
from code_pilot_cli.commands.enhance import enhance
from code_pilot_cli.commands.scan import scan


command_list = [ai, chat, completions, enhance, scan]
