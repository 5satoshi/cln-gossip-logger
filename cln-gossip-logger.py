#!/usr/bin/env python3
from pyln.client import Plugin
import json
import logging
import os
import sys
import time
import psutil

plugin = Plugin()

root = logging.getLogger()
root.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

@plugin.hook('db_write')
def on_db_write(writes, data_version, plugin, **kwargs):
    
    if True:
        return {"result": "continue"}
    else:
        kill("Error: cl-gossip-logger caused an critical error. Need to shutdown!")

@plugin.init()
def on_init(options, **kwargs):
        plugin.log(
            "cl-gossip-logger initiated",
            level="warn"
        )


if __name__ == "__main__":
    # Did we perform the first write check?
    plugin.initialized = False
    if not os.path.exists("cln-gossip-logger.lock"):
        kill("Could not find cln-gossip-logger.lock in the lightning-dir")

    try:
        d = json.load(open("cln-gossip-logger.lock", 'r'))
        destination = d['gbq-destination']
        plugin.run()
    except Exception:
        logging.exception('Exception while initializing cln-gossip-logger plugin')
        kill('Exception while initializing plugin, terminating lightningd')
