"""
    Provide command `wemoo`
"""

import os
import sys
import traceback

from daemonize import Daemonize

from wemoo_agent.config.config import config
from wemoo_agent.core.hosts import login_or_register_host
from wemoo_agent.core.produce import Eventloop
from wemoo_agent.system import shell

HELP = """

Run command like:
$ wemoo start|stop|run

DESCRIPTION:
- start\tStart daemon;
- stop\tStop daemon process running in the background;
- run\tRun in terminal instesd of background.
"""


def run():
    # register device
    if not login_or_register_host():
        sys.exit("Regist failed.")

    event = Eventloop(config)
    event.event_loop()


def main():
    global HELP
    if len(sys.argv) < 2:
        sys.exit('Parameter is missing.' + HELP)

    # whether daemon or not
    try:
        action = sys.argv[1]
        daemon = Daemonize(app="Wemoo Agent", pid=config.pid_file, action=run)

        if action == 'run':
            run()
        elif action == 'start':
            daemon.start()
            print('Start daemon.')
        elif action == 'stop':
            result = shell.exec_shell_script('kill `cat ' + config.pid_file + '`')
            if (result == b''):
                print('Exit daemon.')
            else:
                print('Fail to stop.')
    except KeyboardInterrupt:
        print("\nExited.")
    except Exception as inst:
        print('Launch failed.')
        traceback.print_exc()
