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


def kill(session):
    p = subprocess.Popen("tmux kill-session -t {}".format(session),
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         shell=True)
    out, err = p.communicate()
    if "session not found" in err:
        raise SessionDoesNotExist(session)
    if "failed to connect to server" in err:
        raise ServerConnectionError()


def list():
    p = subprocess.Popen("tmux ls",
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         shell=True)
    out, err = p.communicate()
    if "failed to connect to server" in err:
        raise ServerConnectionError()
    return out

def create(session):
    p = subprocess.Popen("tmux new -s {}".format(session),
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         shell=True)
    out, err = p.communicate()

    if "duplicate session" in err:
        raise SessionExists(session)


def attach(session):
    p = subprocess.Popen("tmux a -t {}".format(session),
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE,
                     shell=True)
    out, err = p.communicate()

    if "no sessions" in err:
        raise SessionDoesNotExist(session)

def create_or_attach(session):
    try:
        create(session)
    except SessionExists:
        attach(session)