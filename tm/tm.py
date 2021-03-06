#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import argparse
import tmux_wrapper as tmux
import sessions

__version__ = 1.0
__description__ = "A command-line tmux wrapper featuring shortcuts and JSON-configurable session presets."


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

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
    parser.add_argument("-r", "--restart",
                        action="store_true",
                        help="kill sessions running under the same name "
                             "when starting a session")

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
            print tmux.list(),
        except tmux.ServerConnectionError, e:
            print(e.description)
    elif args.session:
        # print("Creating and configuring session...")
        if args.restart:
            try:
                tmux.kill(args.session)
            except (tmux.ServerConnectionError, tmux.SessionDoesNotExist):
                pass
            tmux.create(args.session)
            sessions.load_session_preset(args.session)
            tmux.attach(args.session)
        else:
            # if session was created
            if tmux.create_or_attach(args.session):
                sessions.load_session_preset(args.session)
                tmux.attach(args.session)

if __name__ == "__main__":
    main(sys.argv[1:])
