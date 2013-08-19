# -*- coding: utf-8 -*-

from collections import deque
import json
import os
import time
import tmux_wrapper as tmux

id_counter = 0

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


def mark_panes(data):
    global id_counter

    if "split" not in data:
        if "id" not in data:
            data["id"] = id_counter
            id_counter += 1
        return data
    else:
        for i, pane in enumerate(data["panes"]):
            inc = False
            if "id" not in pane:
                data["panes"][i]["id"] = id_counter
                inc = True
            if "panes" in pane:
                data["panes"][i]["panes"][0]["id"] = id_counter
                inc = True
            if inc:
                id_counter += 1


        for i, pane in enumerate(data["panes"]):
            data["panes"][i] = mark_panes(pane)
        return data


def make_pane_set(data):
    if "split" not in data:
        if "commands" in data:
            for command in data["commands"]:
                tmux.run_shell_command(data["id"], command)
        print data
    else:
        cumulative = 0
        for pane in data["panes"]:
            percentage = pane["size"]
            parent_percentage = percentage / (100.0 - cumulative) * 100.0
            cumulative += percentage
            if cumulative < 99:
                tmux.split_window(pane["id"], data["split"], 100 - int(parent_percentage))
            make_pane_set(pane)


def load_session_preset(session):
    global id_counter

    config = load_config()
    if config is None or session not in config:
        return

    first = True
    for name, data in config[session].items():
        id_counter = 0
        if first:
            tmux.rename_window(name)
            first = False
        else:
            tmux.new_window(name)
        data = mark_panes(data)
        make_pane_set(data)
