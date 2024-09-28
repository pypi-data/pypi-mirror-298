# -*- coding: utf-8 -*-
# @Time    : 2024/05/14 11:47
# @Author  : Ultipa
# @Email   : support@ultipa.com
# @File    : Index.py
from typing import List

from ultipa.structs import DBType
from ultipa.structs.BaseModel import BaseModel


class Job(BaseModel):
    '''
        Data class for Index.
    '''

    def __init__(self, id: str, graph: str ='',
                 type: str='',
                 uql: str='',
                 gql: str='',
                 status: str='',
                 error: str='',
                 result: str='',
                 startTime: str='',
                 endTime: str='',
                 progress: str=''):
        self.id = id
        self.graph = graph
        self.type = type
        self.uql = uql
        self.gql = gql
        self.status = status
        self.error = error
        self.result = result
        self.startTime = startTime
        self.endTime = endTime
        self.progress = progress

