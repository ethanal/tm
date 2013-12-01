# -*- coding: utf-8 -*-

import subprocess


class SessionExists(Exception):
    description = "Session already exists."
    pass


class ServerConnectionError(Exception):
    description = "tmux server is not currently running."
    pass


class SessionDoesNotExist(Exception):
    description = "Session does not exist."
    pass

class CommandResponse(object):
    def __init__(self, process):
        self.process = process
        self.out, self.err = process.communicate()


def tmux_command(command):
    p = subprocess.Popen("tmux " + command,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         shell=True)
    r = CommandResponse(p)

    if "session not found" in r.err:
        raise SessionDoesNotExist()
    if "failed to connect to server" in r.err:
        raise ServerConnectionError()
    if "duplicate session" in r.err:
        raise SessionExists()
    if "no sessions" in r.err:
        raise SessionDoesNotExist()

    return r


def kill(session):
    tmux_command("kill-session -t {}".format(session))


def list():
    r = tmux_command("ls")
    return r.out


def create(session):
    tmux_command("new-session -d -s {}".format(session))


def attach(session):
    tmux_command("attach-session -t {}".format(session))


def has_session(session):
    try:
        # default tmux functionality matches prefixes to existing sessions
        # r = tmux_command("has-session -t {}".format(session))
        # return r.process.returncode == 0

        l = tmux_command("ls").out
        sessions = [s.split(" ")[0][:-1] for s in l.split("\n")[:-1]]
        return session in sessions
    except (ServerConnectionError, SessionDoesNotExist):
        return False


def create_or_attach(session):
    if has_session(session):
        attach(session)
        return False
    else:
        create(session)
        return True


def run_shell_command(pane, command):
    tmux_command("send-keys -t {} \"{}\" C-m".format(pane, command))


def new_window(index, name):
    tmux_command("new-window -t {} -n '{}'".format(index, name))


def rename_window(index, name):
    tmux_command("rename-window -t {} {}".format(index, name))


def split_window(pane, direction, percentage):
    # print "splitting {} {} {}".format(pane, direction, percentage)
    tmux_command("split-window -t {} -{} -p {}".format(pane, direction[0], str(percentage)))


def select_pane(pane):
    tmux_command("select-pane -t {}".format(pane))

def select_window(window):
    tmux_command("select-window -t {}".format(window))

