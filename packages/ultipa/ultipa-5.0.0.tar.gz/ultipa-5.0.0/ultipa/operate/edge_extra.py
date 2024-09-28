from typing import List

from ultipa.configuration import InsertRequestConfig
from ultipa.operate.base_extra import BaseExtra
from ultipa.structs import Edge, InsertType

from ultipa.types import ULTIPA_REQUEST, ULTIPA, ULTIPA_RESPONSE
from ultipa.utils import UQLMAKER, CommandList
from ultipa.configuration.RequestConfig import RequestConfig
from ultipa.structs.InsertType import InsertType
from ultipa.configuration.InsertConfig import InsertConfig
from ultipa.configuration.InsertRequestConfig import InsertRequestConfig
from ultipa.structs.Edge import Edge
from ultipa.utils.ufilter.new_ufilter import *


class EdgeExtra(BaseExtra):
	'''
	Processing class that defines settings for edge related operations.

	'''

	def searchEdge(self, request: ULTIPA_REQUEST.SearchEdge,
				   requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseSearchEdge:
		'''
		Query for edges.

		Args:
			request: An object of SearchEdge class 

			requestConfig: An object of RequestConfig class

		Returns:
			ResponseSearchEdge

		'''

		uqlMaker = UQLMAKER(command=CommandList.edges, commonParams=requestConfig)
		if request.id:
			uqlMaker.setCommandParams(request.id)
		elif request.filter:
			uqlMaker.setCommandParams(request.filter)

		uqlMaker.addParam('as', request.select.aliasName)
		uqlMaker.addParam("return", request.select)

		res = self.uqlSingle(uqlMaker)
		if res.status.code != ULTIPA.Code.SUCCESS:
			return res
		return res

	def insertEdges(self,edges: List[Edge], schemaName: str, config:InsertRequestConfig) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Insert edges.

		Args:
			edges: List of edges to be inserted

			schemaName: Name of the schema

			config: An object of InsertRequestConfig class

		Returns:
			ResponseInsertEdge
		'''
		combined_values = []  # to combine values and id for insertion
		for edge in edges:
			edge_dict = {}
			if edge._from:
				edge_dict["_from"] = edge._from
			if edge._to:
				edge_dict["_to"]= edge._to

			if edge._from_uuid:
				edge_dict["_from_uuid"]	=edge._from_uuid
			if edge._to_uuid:
				edge_dict["_to_uuid"]=edge._to_uuid

			if edge._uuid:
				edge_dict["_uuid"]=edge._uuid
			edge_dict.update(edge.values)
			combined_values.append(edge_dict)
		edges=combined_values
		schemaName = '@' + schemaName

		uqlMaker = UQLMAKER(command=CommandList.insert, commonParams=config)
		if config.insertType==InsertType.UPSERT:
			uqlMaker = UQLMAKER(command=CommandList.upsert, commonParams=config)
		if config.insertType==InsertType.OVERWRITE:
			uqlMaker.addParam('overwrite', "", required=False)
		if schemaName:
			uqlMaker.addParam('into', schemaName, required=False)
		uqlMaker.addParam('edges', edges)

		if config.silent==False:
			uqlMaker.addParam('as', "edges")
			# uqlMaker.addParam('return', "edges._uuid")
			uqlMaker.addParam('return', "edges{*}")
		res = self.uqlSingle(uqlMaker)
		if res.status.code != ULTIPA.Code.SUCCESS:
			return res
		if config.silent==False:
			if len(res.aliases) > 0:
				res.data = res.items.get(res.aliases[0].alias).data
		return res

	def updateEdges(self, request: ULTIPA_REQUEST.UpdateEdge,
				   requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Update edges.

		Args:
			request: An object of UpdateEdge class

			requestConfig: An object of RequestConfig class

		Returns:
			UltipaResponse

		'''

		uqlMaker = UQLMAKER(command=CommandList.updateEdges, commonParams=requestConfig)
		if request.id:
			uqlMaker.setCommandParams(request.id)
		elif request.filter:
			uqlMaker.setCommandParams(request.filter)
		uqlMaker.addParam("set", request.values)
		uqlMaker.addParam("silent", request.silent)
		res = self.UqlUpdateSimple(uqlMaker)
		return res

	def deleteEdges(self, filter: str, config: InsertRequestConfig) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Delete edges.

		Args:
			filtert: An object of UltipaFilter class

			config: An object of InsertConfig class

		Returns:
			ResponseDeleteEdge

		'''

		uqlMaker = UQLMAKER(command=CommandList.deleteEdges, commonParams=config)
		# if request.id:
		# 	uqlMaker.setCommandParams(request.id)
		if filter:
			uqlMaker.setCommandParams(filter)

		if config.silent == False:
			uqlMaker.addParam('as', "edges")
			# uqlMaker.addParam('return', "edges._uuid")
			uqlMaker.addParam('return', "edges{*}")

		res = self.uqlSingle(uqlMaker)
		if res.status.code == ULTIPA.Code.SUCCESS:
			if config.silent == False:
				if len(res.aliases) > 0:
					if len(res.items) > 0:
						res.data = res.items.get(res.aliases[0].alias).data
					else:
						return res
			return res
		else:
			return res