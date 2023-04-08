import sys

from firefly_cli._version import get_versions
from firefly_cli.api import FireflyAPI
from firefly_cli.cli import FireflyPrompt
from firefly_cli.parser import Parser
from firefly_cli.transaction import Transaction

__version__ = get_versions()["version"]
del get_versions


def _real_main():

    if len(sys.argv) > 1:
        args, ffargs = Parser.entrypoint().parse_known_args()

        if args.version:
            FireflyPrompt().onecmd("version")
        elif args.help:
            FireflyPrompt().onecmd("help")
        else:
            FireflyPrompt().onecmd(Parser.safe_string(ffargs))
    else:
        FireflyPrompt().cmdloop()


def main():
    try:
        _real_main()
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    except Exception:
        # Silence raising exceptions
        raise
