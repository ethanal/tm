#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import os
import sys
import subprocess
import argparse

__version__ = 1.0
__description__ = "A tmux wrapper featuring shortcuts and session presets."


def parse_common_errors(error):
    if "session not found" in error:
        print("Session not found")
    elif "failed to connect to server" in error:
        print("tmux server not currently running")


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

    err = ""
    out = ""
    if args.kill:
        p = subprocess.Popen("tmux kill-session -t {}".format(args.kill),
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             shell=True)
        out, err = p.communicate()
    elif args.list:
        p = subprocess.Popen("tmux ls",
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             shell=True)
        out, err = p.communicate()
    elif args.session:
        p = subprocess.Popen("tmux new -s {}".format(args.session),
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             shell=True)
        out, err = p.communicate()
        if "duplicate session" in err:
            p = subprocess.Popen("tmux a -t {}".format(args.session),
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             shell=True)
            out, err = p.communicate()

    parse_common_errors(err)
    if out:
        print out.strip()

if __name__ == "__main__":
    main(sys.argv[1:])