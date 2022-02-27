import sys

from ._version import get_versions
from .cli import FireflyPrompt

__version__ = get_versions()["version"]


def _real_main():
    if len(sys.argv) > 1:
        FireflyPrompt().onecmd(" ".join(sys.argv[1:]))
    else:
        FireflyPrompt().cmdloop()


def main():
    try:
        _real_main()
    except KeyboardInterrupt:
        print("\n[ERROR] Interrupted by user")
    except:
        print("\n[ERROR] Fatal error occurred and firefly-cli cannot continue...")
        raise


from . import _version

__version__ = _version.get_versions()["version"]
