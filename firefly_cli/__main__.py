#!/usr/bin/env python3

# Execute with
# $ python firefly_cli/__main__.py
# $ python -m firefly_cli

import sys

if __package__ is None and not hasattr(sys, "frozen"):
    # Direct call of __main__.py
    import os.path

    path = os.path.realpath(os.path.abspath(__file__))
    sys.path.insert(0, os.path.dirname(os.path.dirname(path)))


if __name__ == "__main__":
    import firefly_cli

    firefly_cli.main()
