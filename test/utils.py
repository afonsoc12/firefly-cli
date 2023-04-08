import json
import sys
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from cmd2.utils import StdSim


def load_test_data(module, file):
    """Loads test data as a dictionary, from the constructed path."""

    test_data_root = Path(__file__).parent.joinpath("test_data")

    file_path = test_data_root / module.split(".")[-1] / file

    if not file_path.is_file():
        raise FileNotFoundError(
            f"Test data file was not found at {file_path.absolute()}"
        )

    with open(file_path, "r") as f:
        return json.loads(f.read())


def ensure_project_root():
    if Path.cwd().parts[-1] != "firefly-cli":
        raise AssertionError(
            f"pytest must run from the source of the repository. Found {Path.cwd().absolute()}"
        )


def run_cmd(app, cmd, skip_normalize=False):
    """Clear out and err StdSim buffers, run the command, and return out and err"""
    saved_sysout = sys.stdout
    sys.stdout = app.stdout

    # This will be used to capture app.stdout and sys.stdout
    copy_cmd_stdout = StdSim(app.stdout)

    # This will be used to capture sys.stderr
    copy_stderr = StdSim(sys.stderr)

    try:
        app.stdout = copy_cmd_stdout
        with redirect_stdout(copy_cmd_stdout):
            with redirect_stderr(copy_stderr):
                app.onecmd_plus_hooks(cmd)
    finally:
        app.stdout = copy_cmd_stdout.inner_stream
        sys.stdout = saved_sysout

    out = copy_cmd_stdout.getvalue()
    err = copy_stderr.getvalue()
    if skip_normalize:
        return out, err
    else:
        return normalize(out), normalize(err)


def normalize(block, remove_empty=False):
    """Normalize a block of text to perform comparison.
    Strip newlines from the very beginning and very end  Then split into separate lines and strip trailing whitespace
    from each line.
    """
    assert isinstance(block, str)
    block = block.strip("\n")
    if not remove_empty:
        return [line.rstrip() for line in block.splitlines()]
    else:
        return [line.rstrip() for line in block.splitlines() if line.rstrip()]
