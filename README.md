# tm

A command-line tmux wrapper featuring shortcuts and JSON-configurable session presets.

## Installation

Install using the setup.py script (may need root).

```bash
$ python setup.py install
```

## Usage

```
tm [-h] [-l] [-k session] [-r] [session]

positional arguments:
  session               the name of the tmux session to start or attach

optional arguments:
  -h, --help            show help message and exit
  -l, --list            list all open sessions and session presets
  -k session, --kill session
                        kill a session
  -r, --restart         kill sessions running under the same name when
                        starting a session
```

### Examples

```bash
$ tm -l           # List all active tmux sessions.
$ tm foobar       # Start a new session named `foobar`. If the session is defined
                  # in your configuration file (see below), initialize that session.
$ tm foobar -r    # Kill and restart the session named `foobar` if it already exists.
                  # Otherwise start the session like normal.
$ tm -k foobar    # Kill the session called `foobar`.
```



## Configuration

Session configuration should be stored in the a JSON file set by the `TM_SESSIONS` environmental variable (e.g. `TM_SESSIONS=~/.tm_config.json`).

The session config file should have the following format:

```js
{
  "<session name>": {

    "<window name>": {
      "commands": ["<command>", "<command>", "<command>"]
    },

    "<window name>": {
      "split": "<horizontal|vertical>",
      "panes": [
        {
          "size": <percent>,
          "split": "<horizontal|vertical>",
          "panes": [
            {
              "size": <percent>,
              "commands": ["<command>", "<command>"]
            }
          ]
        },
        {
          "size": <percent>,
          "commands": ["<command>"]
        }
      ]
    }
  }
}
```

At the top level, there can be any number of unique sessions keyed by session name. In each session there are windows, keyed by window name and loaded in order of appearance in the config file. A window can be thought of as a tree of pane nodes and is comprised of a single pane or many nested panes. Windows can be split into multiple panes, either horizontally or vertically (indicated by the `split` key), each sized by the `size` key. `size` should be specified as a percent of the parent pane's dimension in the `split` direction specified without a "%" sign. The sizes of each pane within a parent pane should add up to 100. If a pane has child panes, the children must be configured according to the same specifications. If a pane has no child panes and isn't a child of a window, a `size` key must be specified. Optionally, leaf nodes of the pane tree may contain a list of `commands` to run on launch.
