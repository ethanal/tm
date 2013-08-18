#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import os
import sys
import argparse
import tmux_wrapper as tmux

__version__ = 1.0
__description__ = "A tmux wrapper featuring shortcuts and session presets."


def load_session_presets():
    try:
        file_path = os.environ["TM_SESSIONS"]
    except KeyError:
        return None

    try:
        with open(file_path) as f:
            config = json.load(f)
    except IOError:
        print("Invalid TM_SESSIONS environmental variable: cannot open file {}".format(file_path))

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


    if len(argv) == 0:
        parser.print_help()

    if args.kill:
        try:
            tmux.kill(args.kill)
        except (tmux.ServerConnectionError, tmux.SessionDoesNotExist), e:
            print(e.description)
    elif args.list:
        try:
            print tmux.list()
        except tmux.ServerConnectionError, e:
            print(e.description)
    elif args.session:
        tmux.create_or_attach(args.session)

if __name__ == "__main__":
    main(sys.argv[1:])