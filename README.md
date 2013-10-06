tm
==

A tmux wrapper featuring shortcuts and session presets.

Configuration
-------------

Session configuration should be stored in the a JSON file set by the `TM_SESSIONS` envoronmental variable (e.g. `TM_SESSIONS=~/.tm_config.json`).

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
