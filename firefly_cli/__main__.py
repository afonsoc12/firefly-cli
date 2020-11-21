import sys
from .cli import FireflyPrompt


def main():
    if len(sys.argv) > 1:
        FireflyPrompt().onecmd(' '.join(sys.argv[1:]))
    else:
        FireflyPrompt().cmdloop()


if __name__ == "__main__":
    sys.exit(main())
