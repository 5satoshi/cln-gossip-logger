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
    plugin.log("hello im in the on_db_write hook, writes array size: {size}".format(size=len(writes)),level="warn")
    plugin.log("print the writes: {writes}".format(writes=writes),level="warn")
    if True:
        return {"result": "continue"}
    else:
        kill("Error: cl-gossip-logger caused an critical error. Need to shutdown!")

@plugin.init()
def on_init(options, **kwargs):
        plugin.log("cl-gossip-logger initiated",level="warn")

def kill(message: str):
    plugin.log(message)
    time.sleep(1)
    # Search for lightningd in my ancestor processes:
    procs = [p for p in psutil.Process(os.getpid()).parents()]
    for p in procs:
        if p.name() != 'lightningd':
            continue
        plugin.log("Killing process {name} ({pid})".format(
            name=p.name(),
            pid=p.pid
        ))
        p.kill()
    
    # Sleep forever, just in case the master doesn't die on us...
    while True:
        time.sleep(30)

if __name__ == "__main__":
    #if not os.path.exists("cln-gossip-logger.lock"):
    #    kill("Could not find cln-gossip-logger.lock in the lightning-dir")
    
    try:
        #d = json.load(open("cln-gossip-logger.lock", 'r'))
        #destination = d['gbq-destination']
        plugin.run()
    except Exception:
        logging.exception('Exception while initializing cln-gossip-logger plugin')
        kill('Exception while initializing plugin, terminating lightningd')
