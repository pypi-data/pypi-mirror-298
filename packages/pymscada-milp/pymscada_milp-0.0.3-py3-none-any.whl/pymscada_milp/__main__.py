"""Provides `python -m pymscada` and `pymscada.exe`."""
from pymscada_milp.main import run


def cmd_line():
    """Run from commandline."""
    run()


if __name__ == '__main__':
    """Starts with creating an event loop."""
    run()
