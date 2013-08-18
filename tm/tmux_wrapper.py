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


def command(command):
    p = subprocess.Popen("tmux " + command,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         shell=True)
    return CommandResponse(p)

def kill(session):
    r = command("kill-session -t {}".format(session))

    if "session not found" in r.err:
        raise SessionDoesNotExist(session)
    if "failed to connect to server" in r.err:
        raise ServerConnectionError()


def list():
    r = command("ls")

    if "failed to connect to server" in r.err:
        raise ServerConnectionError()
    return r.out

def create(session):
    r = command("new -s {}".format(session))

    if "duplicate session" in r.err:
        raise SessionExists(session)


def attach(session):
    r = command("attach-session -d -t {}".format(session))

    if "no sessions" in r.err:
        raise SessionDoesNotExist(session)


def has_session(session):
    r = command("has-session -t {}".format(session))
    return r.process.returncode == 0


def create_or_attach(session):
    if has_session(session):
        attach(session)
        return False
    else:
        create(session)
        return True
