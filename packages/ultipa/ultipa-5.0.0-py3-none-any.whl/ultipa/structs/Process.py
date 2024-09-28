# -*- coding: utf-8 -*-
# @Time    : 2024/05/14 11:47
# @Author  : Ultipa
# @Email   : support@ultipa.com
# @File    : Index.py
from typing import List

from ultipa.structs import DBType
from ultipa.structs.BaseModel import BaseModel


class Process(BaseModel):
    '''
        Data class for Index.
    '''

    def __init__(self, id: str,
                 uql: str,
                 gql: str,
                 duration: int,
                 status: str):
        self.id = id
        self.type = type
        self.uql = uql
        self.gql = gql
        self.duration = duration
        self.status = status

