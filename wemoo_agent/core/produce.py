# -*- coding: utf-8 -*-
"""
    The core service, do the main business.
"""

from time import sleep
from wemoo_agent.core.task import Task
from wemoo_agent.config.config import config


class Eventloop(object):
    def __init__(self, config):
        self.task = Task(config)

    def event_loop(self):
        while (True):
            self.task.check_for_updates()
            self.task.handle()
            self.task.send_back_data()
            self.task.sleep()
            print('another loop')
            sleep(config.interval)
