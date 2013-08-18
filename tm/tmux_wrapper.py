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


def command(command):
    p = subprocess.Popen("tmux " + command,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         shell=True)
    return p.communicate()

def kill(session):
    out, err = command("kill-session -t {}".format(session))

    if "session not found" in err:
        raise SessionDoesNotExist(session)
    if "failed to connect to server" in err:
        raise ServerConnectionError()


def list():
    out, err = command("ls")

    if "failed to connect to server" in err:
        raise ServerConnectionError()
    return out

def create(session):
    out, err = command("new -s {}".format(session))

    if "duplicate session" in err:
        raise SessionExists(session)


def attach(session):
    out, err = command("attach-session -t {}".format(session))

    if "no sessions" in err:
        raise SessionDoesNotExist(session)


def create_or_attach(session):
    try:
        create(session)
    except SessionExists:
        attach(session)

