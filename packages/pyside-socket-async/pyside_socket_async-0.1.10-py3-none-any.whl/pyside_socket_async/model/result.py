#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   result.py
@Time    :   2024-08-15 12:30:13
@Author  :   chakcy 
@Email   :   947105045@qq.com
@description   :   任务结果模型
'''

from pydantic import BaseModel, model_validator, Field, computed_field
from typing import Union
from ..constants import TaskStatus

class Result(BaseModel):
    task_name: str = Field(title="task_name", 
                           default="Task 任务名称")
    status: TaskStatus = Field(title="status",
                        description="Task的执行状态，包括 PENDING、RUNNING、SUCCEEDED、FAILED 四种")
    result: Union[dict, str] = Field(title="result",
                                     description="执行结果")
    id: str = Field(title="id",
                    description="执行结束返回的 Task id 用于在 TS 类中找出对应的回调函数")
    created_at: float = Field(title="created_at",
                              description="任务开始的时间辍")
    updated_at: float = Field(title="updated_at",
                              default="任务状态更新的时间一般为任务结束时间辍")

    @model_validator(mode="after")
    def check_result(self):
        """检查任务执行结果是否正确"""
        if self.status != TaskStatus.SUCCEEDED:
            raise ValueError("Task Failed, please check the log for details.")
        return self
    
    @computed_field  # 计算属性
    @property
    def execution_duration(self) -> float:
        """计算任务执行时间(秒)，时间基于 UTC."""
        return self.updated_at - self.created_at
