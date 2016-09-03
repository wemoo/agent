# -*- coding: utf-8 -*-

import os
from bson.json_util import loads

from wemoo_agent.network.request import http_get, http_patch
from wemoo_agent.system import shell
from wemoo_agent.common.util import save_obj, load_obj
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
        if res.status_code >= 400:
            return

        content = loads(res.text)
        try:
            tasks = content.get('content').get('tasks', [])
            self.tasks.extend(tasks)
        except:
            return

        end = time()
        print('duration: ', int(end - start))

        if os.path.isfile(self.config.cache_file):
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
        file = task.get('file', None)
        if file:
            task['result'] = shell.exec_shell_script(file)

    def send_back_data(self):
        """
        send all result, produced by tasks
        """
        print('self.tasks length: ', len(self.tasks))
        while (len(self.tasks) > 0):
            task = self.tasks.pop()
            data = {"id": task['id'], 'result': task['result']}
            url = self.config.server + "/api/tasks"
            response = http_patch(url, data)
            if response is None:
                self.unfinished_tasks.append(task)
            else:
                if (response.status_code is 200):
                    print('remove task')
                else:
                    self.unfinished_tasks.append(task)

        save_obj(self.unfinished_tasks, self.config.cache_file)
        print('len unfinished_tasks: ', len(self.unfinished_tasks))
        print('sent_back_result')

    def sleep(self):
        """
        Sleep for every loop
        """
        sleep(3)
        # sleep(self.config.interval)
        print('sleep 3')
