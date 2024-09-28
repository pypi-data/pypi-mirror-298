# -*- coding: utf-8 -*-
# @Time    : 2023/8/4 16:20
# @Author  : Ultipa
# @Email   : support@ultipa.com
# @File    : Path.py
from typing import Dict, List

from ultipa.structs.Schema import Schema
from ultipa.structs.BaseModel import BaseModel
from ultipa.structs.Edge import Edge
from ultipa.structs.Node import Node


class Path(BaseModel):
	'''
	    Data class for path.
	'''
	# nodeSchemas: Dict[str, Schema] = {}
	# edgeSchemas: Dict[str, Schema] = {}

	nodeUUIDs: List[int]
	edgeUUIDs: List[int]
	def __init__(self,nodeUUIDs: List[int]=None, edgeUUIDs: List[int]=None):
		self.nodeUUIDs = nodeUUIDs
		self.edgeUUIDs = edgeUUIDs

	# def __init__(self, nodes: List[Node], edges: List[Edge], nodeSchemas, edgeSchemas):
	# 	self.nodes = nodes
	# 	self.edges = edges
	# 	self.nodeSchemas = nodeSchemas
	# 	self.edgeSchemas = edgeSchemas


	# def length(self):
	# 	return len(self.edges)
	#
	# def getNodes(self):
	# 	return self.nodes
	#
	# def getEdges(self):
	# 	return self.edges

class PathAlias:
	'''
	    Data class for path with alias.
	'''
	def __init__(self, alias: str, paths: List[Path] = None):
		self.alias = alias
		if paths is None:
			paths = []
		self.paths = paths

	def length(self):
		return len(self.paths)

	def getNodes(self):
		nodes = [i.nodeUUIDs for i in self.paths]
		return nodes

	def getEdges(self):
		edges = [i.edgeUUIDs for i in self.paths]
		return edges