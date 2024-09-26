
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   parallel_tasks.py
@Time    :   2024-04-30 09:36:00
@Author  :   chakcy 
@Email   :   947105045@qq.com
@description   :   并行任务
'''

from concurrent.futures import ThreadPoolExecutor, as_completed


class ParallelTasks:
    def __init__(self, funcs_and_args:list):
        self.funcs_and_args = funcs_and_args
        self.max_workers = len(funcs_and_args) if len(funcs_and_args) < 5 else 5

    def run(self):
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [executor.submit(func, *args) for func, args in self.funcs_and_args]
            results = {future.result().get("task_name"): future.result().get("result") for future in as_completed(futures)}

        return results
