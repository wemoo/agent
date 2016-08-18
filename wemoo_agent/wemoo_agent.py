"""
    Provide command `wemoo`
"""

import os
import sys

from daemonize import Daemonize

from wemoo_agent.config.config import config
from wemoo_agent.core.hosts import login_or_register_host
from wemoo_agent.core.produce import Eventloop


def run():
    event = Eventloop(config)
    event.event_loop()


def main():
    # register device
    if not login_or_register_host():
        sys.exit("Regist failed.")
    print('Register host.')

    # whether daemon or not
    if config.debug:
        run()
    else:
        daemon = Daemonize(app="Wemoo Agent", pid=config.pid_file, action=run)
        if os.path.isfile(config.pid_file):
            print('Exit daemon.')
            daemon.exit()
        else:
            print('Start daemon.')
            daemon.start()
