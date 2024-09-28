from typing import List

from ultipa.utils.convert import convertTableToDict
from ultipa.structs.Job import Job
from ultipa.types.types import TruncateType
from ultipa.operate.base_extra import BaseExtra
from ultipa.utils import UQLMAKER, CommandList
from ultipa.types import ULTIPA_REQUEST, ULTIPA, ULTIPA_RESPONSE
from ultipa.configuration.RequestConfig import RequestConfig

JSONSTRING_KEYS = ["graph_privileges", "system_privileges", "policies", "policy", "privilege"]
formatdata = ['graph_privileges']


class TruncateExtra(BaseExtra):
    
	'''
        Processing class that defines settings for advanced operations on graphset.
	'''

	def truncate(self, request: ULTIPA_REQUEST.Truncate,
				 requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseCommon:
		'''
		Truncate graphshet.

		Args:
			request: An object of Truncate class

			requestConfig: An object of RequestConfig class

		Returns:
			ResponseCommon

		'''
		command = CommandList.truncate
		requestConfig.graphName = request.graphSetName
		uqlMaker = UQLMAKER(command, commonParams=requestConfig)
		uqlMaker.addParam("graph", request.graphSetName)
		if request.dbType:
			if request.dbType == TruncateType.NODES:
				if request.all:
					uqlMaker.addParam("nodes", "*")
				if not request.all and request.schema:
					uqlMaker.addParam("nodes", "@" + request.schema, notQuotes=True)
			if request.dbType == TruncateType.EDGES:
				if request.all:
					uqlMaker.addParam("edges", "*")
				if not request.all and request.schema:
					uqlMaker.addParam("edges", "@" + request.schema, notQuotes=True)

		# if request.all and not request.dbType:
		#     uqlMaker = UQLMAKER(command,commandP=request.dbType,commonParams=requestConfig)

		return self.UqlUpdateSimple(uqlMaker)

	def compact(self, graphName: str,
				requestConfig: RequestConfig = RequestConfig()) -> Job:
		'''
		Compact graphshet.

		Args:
			graph: The name of graphset

			requestConfig: An object of RequestConfig class

		Returns:
			ResponseCommon

		'''
		command = CommandList.compact
		uqlMaker = UQLMAKER(command, commonParams=requestConfig)
		uqlMaker.addParam("graph", graphName)
		result=self.uqlSingle(uqlMaker)
		if result.items:
			res = convertTableToDict(result.alias("result").data.rows, result.alias("result").data.headers)
			return Job(id=res[0]['new_job_id'])
		else :
			return Job(id='',error=result.status.message)


	def mountGraph(self, graphName: str,
				   requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Mount graphshet.

		Args:
			graph: The name of graphset

			requestConfig: An object of RequestConfig class

		Returns:
			Response

		'''
		commonP = []
		if graphName:
			commonP = graphName
			requestConfig.graphName = graphName
		uqlMaker = UQLMAKER(command=CommandList.mount, commonParams=requestConfig)
		uqlMaker.setCommandParams(commandP=commonP)
		return self.uqlSingle(uqlMaker)

	def unmountGraph(self, graphName: str,
					 requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Unmount graphshet.

		Args:
			graph: The name of graphset

			requestConfig: An object of RequestConfig class

		Returns:
			Response

		'''
		commonP = []
		if graphName:
			commonP = graphName
			requestConfig.graphName = graphName
		uqlMaker = UQLMAKER(command=CommandList.unmount, commonParams=requestConfig)
		uqlMaker.setCommandParams(commandP=commonP)
		return self.uqlSingle(uqlMaker)
