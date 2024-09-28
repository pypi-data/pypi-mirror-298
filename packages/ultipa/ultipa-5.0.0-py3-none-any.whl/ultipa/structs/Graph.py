# -*- coding: utf-8 -*-
# @Time    : 2023/8/1 10:47
# @Author  : Ultipa
# @Email   : support@ultipa.com
# @File    : Graph.py
from typing import Dict, List

from ultipa.structs.BaseModel import BaseModel
from ultipa.structs.Path import Path
from ultipa.structs.Node import Node
from ultipa.structs.Edge import Edge
class Graph(BaseModel):
	'''
	    Data class for graphset.
	'''

	# def __init__(self, name: str, description: str = None):
	# 	self.name = name
	# 	self.description = description

	def __init__(self, paths: Path = None,nodes: Dict[int , Node] = None,
				 edges: Dict[int , Edge] = None):
		self.paths = paths
		self.nodes = nodes
		self.edges = edges

class GraphAlias(BaseModel):
	def __init__(self,  alias: str, graph: List[Graph] = None):
		self.alias = alias
		self.graph = graph

	# id: str
	# name: str
	# totalNodes: str
	# totalEdges: str
	# description: str
	# status: str
	#
	# # def __init__(self, name: str, description: str = None):
	# # 	self.name = name
	# # 	self.description = description
	#
	# def __init__(self, name: str, id: int = None, totalNodes: int = None,
	# 			 totalEdges: int = None, description: str = None, status: str = None):
	# 	self.id = id
	# 	self.name = name
	# 	self.totalNodes = totalNodes
	# 	self.totalEdges = totalEdges
	# 	self.description = description
	# 	self.status = status

