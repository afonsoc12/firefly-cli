import sys

from firefly_cli._version import get_versions
from firefly_cli.cli import FireflyPrompt

__version__ = get_versions()["version"]


def _real_main():

    if len(sys.argv) > 1:
        try:
            FireflyPrompt().onecmd(" ".join(sys.argv[1:]))
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
        pass

