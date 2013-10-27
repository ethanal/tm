# -*- coding: utf-8 -*-

from collections import OrderedDict
import json
import os
import tmux_wrapper as tmux
import pprint

id_counter = 0

def load_config():
    try:
        file_path = os.environ["TM_SESSIONS"]
    except KeyError:
        return None

    try:
        with open(file_path) as f:
            return json.load(f, object_pairs_hook=OrderedDict)
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
            if "id" not in pane and "panes" not in pane:
                data["panes"][i]["id"] = id_counter
                id_counter += 1
            elif "panes" in pane:
                data["panes"][i]["panes"][0]["id"] = id_counter
                id_counter += 1

        for i, pane in enumerate(data["panes"]):
            data["panes"][i] = mark_panes(pane)
        return data

def make_pane_set(data):
    if "split" not in data:
        if "commands" in data:
            for command in data["commands"]:
                tmux.run_shell_command(data["id"], command)
    else:
        cumulative = 0
        for pane in data["panes"]:
            percentage = pane["size"]
            parent_percentage = percentage / (100.0 - cumulative) * 100.0
            cumulative += percentage
            if "id" in pane and cumulative != 100:
                tmux.split_window(pane["id"],
                                  data["split"],
                                  100 - int(parent_percentage))
            make_pane_set(pane)


def load_session_preset(session):
    global id_counter

    config = load_config()
    if config is None or session not in config:
        return

    window_index = 0
    for name, data in config[session].items():
        id_counter = 0
        if window_index == 0:
            tmux.rename_window(window_index, name)
        else:
            tmux.new_window(window_index, name)
        data = mark_panes(data)
        #pprint.PrettyPrinter().pprint(dict(data))

        make_pane_set(data)
        window_index += 1
    tmux.select_window(0)
