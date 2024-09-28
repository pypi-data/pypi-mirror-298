from ultipa.operate.base_extra import BaseExtra
from ultipa.structs import DBType
from ultipa.types import ULTIPA_REQUEST, ULTIPA, ULTIPA_RESPONSE
from ultipa.utils import UQLMAKER, CommandList
from ultipa.configuration.RequestConfig import RequestConfig

class LteUfeExtra(BaseExtra):

	'''
	Processsing class that defines settings for LTE and UFE related operations.
	'''

	def lte(self, request: ULTIPA_REQUEST.LTE,
			requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Load properties to memory (LTE).

		Args:
			request: An object of LTE class
			requestConfig: An object of RequestConfig class

		Returns:
			UltipaResponse
		'''

		command = request.type == DBType.DBNODE and CommandList.lteNode or CommandList.lteEdge
		uqlMaker = UQLMAKER(command=command, commonParams=requestConfig)
		uqlMaker.setCommandParams(request.schemaName.toString)
		res = self.uqlSingle(uqlMaker=uqlMaker)
		return res

	def ufe(self, request: ULTIPA_REQUEST.UFE,
			requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Unload properties from memory (UFE).

		Args:
			request: An object of UFE class
			requestConfig: An object of RequestConfig class

		Returns:
			UltipaResponse
		'''

		command = request.type == DBType.DBNODE and CommandList.ufeNode or CommandList.ufeEdge
		uqlMaker = UQLMAKER(command=command, commonParams=requestConfig)
		uqlMaker.setCommandParams(request.schemaName.toString)
		res = self.uqlSingle(uqlMaker=uqlMaker)
		return res
