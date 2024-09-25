# -*- coding: utf-8 -*-
# @Time : 2023/07/04
# @Author : chengwenping2

class InterfaceFrameCaseException(Exception):
    def __init__(self, description, case_name, check_detail, use_time):
        self.description = description
        self.case_name = case_name
        self.check_detail = check_detail
        self.use_time = use_time
        super(InterfaceFrameCaseException, self)


class InterfaceFrameCaseStopException(Exception):
    def __init__(self, stop_reason: str):
        self.stop_reason = stop_reason
        super(InterfaceFrameCaseStopException, self)
