
import warnings
import traceback
import sys
import subprocess
import logging
from simple_chalk import red, green, yellow


SUPPORTED_COMMANDS = [
    "write",
    "open",
    "help",
    "exit"
]


SUPPORTED_COMMAND_LIST = "\n".join(
    list(map(lambda x: green.bold(x), SUPPORTED_COMMANDS))
)

HELP_MESSAGE = f"Here are the supported commands\n{SUPPORTED_COMMAND_LIST}"


logger = logging.getLogger(__name__)


class CommandNotSupported(Exception):
    pass


_formatwarning = warnings.formatwarning


def formatwarning_tb(*args, **kwargs):
    s = _formatwarning(*args, **kwargs)
    tb = traceback.format_stack()
    s += ''.join(tb[:-1])
    return s


warnings.formatwarning = formatwarning_tb
logging.captureWarnings(True)


def pretty_print_error(message: str) -> None:
    print(red(message))


def handle_write(argument: list) -> None:
    print(*argument)


def handle_help() -> None:
    print(HELP_MESSAGE)


def handle_exit(message: str = "") -> None:
    if message:
        print(yellow(message))
    sys.exit()


def handle_open(argument: list) -> None:

    updated_arguments = ["open", *argument]

    feedback = subprocess.Popen(updated_arguments)

    if feedback != None:
        pretty_print_error("Unable to open")


def is_supported_command(command: str) -> bool:
    # Check if the command is supported
    return command in SUPPORTED_COMMANDS


def breakdown_command(command: str) -> list:
    # Breakdown the command into a list of arguments
    return command.split(" ")


def handle_input(input: str) -> None:
    [action, *argument] = breakdown_command(input)

    if not is_supported_command(action):
        logger.debug(f"Command ${action} not supported")
        raise CommandNotSupported(f"Command {action} not supported")

    match action:
        case "exit":
            handle_exit("Exiting application")

        case "help":
            handle_help()

        case "open":
            handle_open(argument=argument)

        case "write":
            handle_write(argument=argument)

        case _:
            raise NotImplementedError(f"Command {action} not implemented")


def request_input() -> str:
    # Request input from the user via the terminal
    return input("Enter command: ")


def run() -> None:

    # instantiate logger instance

    # This will operate like a REPL
    # It constantly accepts commands from the terminal and processes them
    while True:

        try:

            input = request_input()
            handle_input(input)

        except KeyboardInterrupt:
            logger.debug("Keyboard interrupt detected")
            handle_exit("Exiting application")

        except Exception as e:
            logger.error(e)
            pretty_print_error(e)


if __name__ == "__main__":
    run()
