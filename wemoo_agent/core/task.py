# -*- coding: utf-8 -*-

import os
from bson.json_util import loads

from wemoo_agent.network.request import http_get, http_patch
from wemoo_agent.system import shell
from wemoo_agent.common.util import save_obj, load_obj
from wemoo_agent.config.config import config
from multiprocessing.dummy import Pool as ThreadPool
from time import time
from time import sleep


class Task(object):
    def __init__(self, config):
        self.config = config
        self.unfinished_tasks = []
        self.finished_tasks = []
        self.tasks = []

    def check_for_updates(self):
        """
        Check for new update and sync to local DB
        TODO: if self.config.server is None, try to log
        """
        if self.config.server is None:
            print('config error')
            return None

        request_tasks_url = self.config.server + '/api/tasks'
        print('start request', request_tasks_url)
        start = time()

        res = http_get(request_tasks_url)
        json = res.json()
        if not json.get('success'):
            return

        try:
            tasks = json.get('content').get('tasks', [])
            self.tasks.extend(tasks)
        except:
            return

        end = time()
        print('duration: ', int(end - start))

        if os.path.isfile(self.config.cache_file) and config.debug:
            try:
                self.unfinished_tasks = load_obj(self.config.cache_file)
                save_obj([], self.config.cache_file)
            except:
                print('load object from file error')
        self.tasks.extend(self.unfinished_tasks)
        self.unfinished_tasks = []

    def handle(self):
        """
        Execute the tasks on localhost
        """
        pool = ThreadPool(10)
        pool.map(self.run_command, self.tasks)
        pool.close()
        pool.join()

    def run_command(self, task):
        # TODO: handle task run fail
        script = task.get('script', None)
        if script:
            task['result'] = shell.exec_shell_script(script).decode('utf-8')

    def send_back_data(self):
        """
        send all result, produced by tasks
        """
        print('self.tasks length: ', len(self.tasks))
        while (len(self.tasks) > 0):
            task = self.tasks.pop()
            data = {"id": task['id'], 'result': task['result']}
            url = self.config.server + '/api/tasks/' + task['id'] + '/exec'
            response = http_patch(url, data)
            if response is None:
                self.unfinished_tasks.append(task)
            else:
                if (response.status_code is 200):
                    print('remove task')
                else:
                    self.unfinished_tasks.append(task)

        if config.debug:
            save_obj(self.unfinished_tasks, self.config.cache_file)
        print('len unfinished_tasks: ', len(self.unfinished_tasks))
        print('sent_back_result')

    def sleep(self):
        """
        Sleep for every loop
        """
        print('sleep for interval')
        sleep(self.config.interval)
