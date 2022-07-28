import sys

from firefly_cli._version import get_versions
from firefly_cli.cli import FireflyPrompt
from firefly_cli.parser import Parser

__version__ = get_versions()["version"]


def _real_main():

    if len(sys.argv) > 1:
        args, ffargs = Parser.entrypoint().parse_known_args()

        try:
            if args.version:
                FireflyPrompt().onecmd("version")
            elif args.help:
                FireflyPrompt().onecmd("help")
            else:
                FireflyPrompt().onecmd(" ".join(ffargs))
        except Exception:
            raise
    else:
        FireflyPrompt().cmdloop()


def main():
    try:
        _real_main()
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    except:
        # Silence raising exceptions
        raise
        # pass
