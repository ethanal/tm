# -*- coding: utf-8 -*-
import json
import os
import tmux_wrapper as tmux


def load_config():
    try:
        file_path = os.environ["TM_SESSIONS"]
    except KeyError:
        return None

    try:
        with open(file_path) as f:
            return json.load(f)
    except IOError:
        print("Invalid TM_SESSIONS environmental variable: "
              "cannot open file {}".format(file_path))
        return None


def load_session_preset(session):
    config = load_config()
    if config is None or session not in config:
        return
