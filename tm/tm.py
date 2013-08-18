#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import subprocess
import argparse

__version__ = 1.0
__description__ = "A tmux wrapper featuring shortcuts and session presets."


def main(argv):
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument("session",
                        metavar="session",
                        type=str,
                        nargs="?",
                        help="the name of the tmux session to start or attach")
    parser.add_argument("-l", "--list",
                        action="store_true",
                        help="list all open sessions and session presets")
    parser.add_argument("-k", "--kill",
                        metavar="session",
                        action="store",
                        help="kill a session")

    args = parser.parse_args()

    err = ""
    if args.kill:
        pass
    elif args.list:
        pass
    elif args.session:
        pass

if __name__ == "__main__":
    main(sys.argv[1:])