## cln-gossip-logger

The gossip-logger plugin for core-lightning allows backing up historic gossip data for a later 
analysis or ml processing. Nodes and channels gossip gets timestamped and stored in bigquery
exclusively (other storing options tbd) as an extended the schema as known from the nodes and channel tables.

## Installation

To install and activate the gossip logger plugin you need to stop your lightningd and restart it
with the `plugin` argument like this:
 
```
lightningd --plugin=/path/to/plugin/directory/cln-gossip-logger.py
```

Important:
 - The `cln-gossip-logger.py` must have executable permissions:
   `chmod a+x cln-gossip.logger.py`

### Automatic plugin initialization

Alternatively, especially when you use multiple plugins, you can copy or symlink
the plugin directory into your `~/.lightning/plugins` directory. The daemon
will load each executable it finds in sub-directories as a plugin. In this case
you don't need to manage all the `--plugin=...` parameters.

#### Minimum supported Python version

The minimum supported version of Python for this repository is currently `3.6.x` (23 Dec 2016).
Python plugins users must ensure to have a version `>= 3.6`.

## Configuration

cln-gossip-logger requires configuration parameters that define the bigquery storage location.
The configuration file gossip-logger.conf must exist in your plugin folder.

```
[bigquery]
nodes = version_1.nodes
channels = version_1.channels
```
