import hashlib
import os


from ultipa.configuration.RequestConfig import RequestConfig
from ultipa.operate.base_extra import BaseExtra
from ultipa.proto import ultipa_pb2
from ultipa.structs.Algo import ALGO_RESULT
from ultipa.types import ULTIPA_REQUEST, ULTIPA, ULTIPA_RESPONSE
from ultipa.utils import UQLMAKER, CommandList, errors
from ultipa.utils.fileSize import read_in_chunks
from ultipa.utils.format import FormatType
from ultipa.utils.ResposeFormat import ResponseKeyFormat
from ultipa.utils.convert import convertToAlgo


class AlgoExtra(BaseExtra):
	'''
		Processing class that defines settings for algorithm related operations.

	'''
	JSONSTRING_KEYS = ["param"]

	def showAlgo(self,
				 requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseListAlgo:
		'''
		Query for algorithm list.

		Args:
			requestConfig: An object of the RequestConfig class

		Returns:
			ResponseListAlgo

		'''
		uqlMaker = UQLMAKER(command=CommandList.showAlgo, commonParams=requestConfig)
		res = self.UqlListSimple(uqlMaker=uqlMaker, responseKeyFormat=ResponseKeyFormat(jsonKeys=self.JSONSTRING_KEYS))
		if res.status.code == ULTIPA.Code.SUCCESS:
			res.data=convertToAlgo(res)
			for algo in res.data:
				try:
					result_opt = int(algo.result_opt) if algo.result_opt is not None else 0
				except Exception as e:
					raise errors.ParameterException(e)
				result_opt_obj = ULTIPA_RESPONSE.AlgoResultOpt()
				result_opt_obj.can_realtime = True if result_opt & ALGO_RESULT.WRITE_TO_CLIENT else False
				result_opt_obj.can_visualization = True if result_opt & ALGO_RESULT.WRITE_TO_VISUALIZATION else False
				result_opt_obj.can_write_back = True if result_opt & (
						ALGO_RESULT.WRITE_TO_DB | ALGO_RESULT.WRITE_TO_FILE) else False
				algo.__setattr__("result_opt", result_opt_obj)
		return res

	def showExta(self,config: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Query for algorithm list.

		Args:
			config: An object of the RequestConfig class

		Returns:
			ResponseListAlgo

		'''
		uqlMaker = UQLMAKER(command=CommandList.showExta, commonParams=config)
		res = self.UqlListSimple(uqlMaker)
		return res

	def __make_message(self, fileName, md5, chunk, hdcName):
		return ultipa_pb2.InstallAlgoRequest(
			file_name=fileName, md5=md5, chunk=chunk, with_server=ultipa_pb2.WithServer(hdc_server_name=hdcName)
		)

	def __generate_messages(self, request: ULTIPA_REQUEST.InstallAlgo):
		messages = []
		file_object = open(request.soPath, 'rb')
		hdcName = request.hdcName
		somd5 = hashlib.md5(file_object.read()).hexdigest()
		file_object.close()

		for chunk in read_in_chunks(request.soPath):
			fileName = os.path.basename(request.soPath)
			messages.append(self.__make_message(fileName, somd5, chunk, hdcName))

		file_object = open(request.configPath, 'rb')
		configmd5 = hashlib.md5(file_object.read()).hexdigest()
		file_object.close()
		for chunk in read_in_chunks(request.configPath):
			fileName = os.path.basename(request.configPath)
			messages.append(self.__make_message(fileName, configmd5, chunk, hdcName))
		for msg in messages:
			yield msg

	def installAlgo(self, soFilePath: str, infoFilePath: str,
					config: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Install an Ultipa standard algorithm.

		Args:
			algoFilePath: The directory of the algorithm package (.so)

			algoInfoFilePath: The directory of the algorithm configuration (.yml)

			requestConfig: An object of the RequestConfig class

		Returns:
			Response

		'''
		request = ULTIPA_REQUEST.InstallAlgo(infoFilePath, soFilePath)
		config.useMaster = True
		clientInfo = self.getClientInfo(graphSetName=config.graphName, useMaster=config.useMaster,
										isGlobal=True)
		response = ULTIPA_RESPONSE.UltipaResponse()
		try:
			if os.path.exists(request.soPath) and os.path.exists(request.configPath):
				installRet = clientInfo.Controlsclient.InstallAlgo(self.__generate_messages(request),
																   metadata=clientInfo.metadata)
				status = FormatType.status(installRet.status)
				response.status = status
		except Exception as e:
			try:
				message = str(e._state.code) + ' : ' + str(e._state.details)
			except:
				message = str(e)

			response.status = ULTIPA.Status(code=ULTIPA.Code.UNKNOW_ERROR, message=message)

		if self.defaultConfig.responseWithRequestInfo:
			response.req = ULTIPA.ReturnReq(self.graphSetName, "InstallAlgo",
											config.useHost if config.useHost else self.host,
											config.retry,
											False)
		return response

	def uninstallAlgo(self, algoName: str,
					  config: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Uninstall an Ultipa standard algorithm.

		Args:
			algoName: The name of algorithm

			requestConfig: An object of the RequestConfig class

		Returns:
			Response

		'''
		config.useMaster = True
		clientInfo = self.getClientInfo(graphSetName=config.graphName, useMaster=config.useMaster,
										isGlobal=True)
		arequest = ultipa_pb2.UninstallAlgoRequest(algo_name=algoName)
		installRet = clientInfo.Controlsclient.UninstallAlgo(arequest, metadata=clientInfo.metadata)
		status = FormatType.status(installRet.status)
		response = ULTIPA_RESPONSE.UltipaResponse(status=status)
		if self.defaultConfig.responseWithRequestInfo:
			response.req = ULTIPA.ReturnReq(self.graphSetName, "UnInstallAlgo",
											config.useHost if config.useHost else self.host,
											config.retry,
											False)
		return response

	# def installExta(self, extaFilePath: str, extaInfoFilePath: str,
	# 					config: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
	# 	'''
	# 	Install an EXTA algorithm (via gRPC port).
	#
	# 	Args:
	# 		extaFilePath: The directory of the exta package (.so)
	#
	# 		extaInfoFilePath: The directory of the exta configuration (.yml)
	#
	# 		config: An object of the RequestConfig class
	#
	# 	Returns:
	# 		Response
	#
	# 	'''
	#
	# 	request = ULTIPA_REQUEST.InstallAlgo(extaInfoFilePath, extaFilePath)
	# 	config.useMaster = True
	# 	clientInfo = self.getClientInfo(graphSetName=config.graphName, useMaster=config.useMaster)
	# 	response = ULTIPA_RESPONSE.UltipaResponse()
	# 	try:
	# 		if os.path.exists(request.soPath) and os.path.exists(request.configPath):
	# 			installRet = clientInfo.Controlsclient.InstallExta(self.__generate_messages(request),
	# 															   metadata=clientInfo.metadata)
	# 			status = FormatType.status(installRet.status)
	# 			response.status = status
	# 	except Exception as e:
	# 		try:
	# 			message = str(e._state.code) + ' : ' + str(e._state.details)
	# 		except:
	# 			message = str(e)
	#
	# 		response.status = ULTIPA.Status(code=ULTIPA.Code.UNKNOW_ERROR, message=message)
	#
	# 	if self.defaultConfig.responseWithRequestInfo:
	# 		response.req = ULTIPA.ReturnReq(self.graphSetName, "InstallExta",
	# 										config.useHost if config.useHost else self.host,
	# 										config.retry,
	# 										False)
	# 	return response
	#
	# def uninstallExta(self, extaName: str,
	# 					  requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
	# 	'''
	# 	Uninstall an EXTA (via gRPC port).
	#
	# 	Args:
	# 		extaName: The name of exta
	#
	# 		requestConfig: An object of the RequestConfig class
	#
	# 	Returns:
	# 		Response
	#
	# 	'''
	# 	requestConfig.useMaster = True
	# 	clientInfo = self.getClientInfo(graphSetName=requestConfig.graphName, useMaster=requestConfig.useMaster)
	# 	arequest = ultipa_pb2.UninstallExtaRequest(exta_name=extaName)
	# 	installRet = clientInfo.Controlsclient.UninstallExta(arequest, metadata=clientInfo.metadata)
	# 	status = FormatType.status(installRet.status)
	# 	response = ULTIPA_RESPONSE.UltipaResponse(status=status)
	# 	if self.defaultConfig.responseWithRequestInfo:
	# 		response.req = ULTIPA.ReturnReq(self.graphSetName, "UninstallExta",
	# 										requestConfig.useHost if requestConfig.useHost else self.host,
	# 										requestConfig.retry,
	# 										False)
	# 	return response

	def installHDCAlgo(self, soFile: str, ymlFile: str,hdcName:str,
					requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.Response:
		'''
		Install an Ultipa standard algorithm.

		Args:
			algoFilePath: The directory of the algorithm package (.so)

			algoInfoFilePat
			h: The directory of the algorithm configuration (.yml)

			requestConfig: An object of the RequestConfig class

		Returns:
			Response

		'''
		request = ULTIPA_REQUEST.InstallAlgo(ymlFile, soFile,hdcName)
		requestConfig.useMaster = True
		clientInfo = self.getClientInfo(graphSetName=requestConfig.graphName, useMaster=requestConfig.useMaster,
										isGlobal=True)
		response = ULTIPA_RESPONSE.Response()
		try:
			if os.path.exists(request.soPath) and os.path.exists(request.configPath):
				installRet = clientInfo.Controlsclient.InstallAlgo(self.__generate_messages(request),
																   metadata=clientInfo.metadata)
				status = FormatType.status(installRet.status)
				response.status = status
		except Exception as e:
			try:
				message = str(e._state.code) + ' : ' + str(e._state.details)
			except:
				message = str(e)

			response.status = ULTIPA.Status(code=ULTIPA.Code.UNKNOW_ERROR, message=message)

		if self.defaultConfig.responseWithRequestInfo:
			response.req = ULTIPA.ReturnReq(self.graphSetName, "InstallAlgo",
											requestConfig.useHost if requestConfig.useHost else self.host,
											requestConfig.retry,
											False)
		return response

	def uninstallHDCAlgo(self, algoName: str,hdcName:str,
					  requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.Response:
		'''
		Uninstall an Ultipa standard algorithm.

		Args:
			algoName: The name of algorithm

			requestConfig: An object of the RequestConfig class

		Returns:
			Response

		'''
		requestConfig.useMaster = True
		clientInfo = self.getClientInfo(graphSetName=requestConfig.graphName, useMaster=requestConfig.useMaster,
										isGlobal=True)
		arequest = ultipa_pb2.UninstallAlgoRequest(algo_name=algoName, with_server=ultipa_pb2.WithServer(hdc_server_name=hdcName))
		installRet = clientInfo.Controlsclient.UninstallAlgo(arequest, metadata=clientInfo.metadata)
		status = FormatType.status(installRet.status)
		response = ULTIPA_RESPONSE.Response(status=status)
		if self.defaultConfig.responseWithRequestInfo:
			response.req = ULTIPA.ReturnReq(self.graphSetName, "UnInstallAlgo",
											requestConfig.useHost if requestConfig.useHost else self.host,
											requestConfig.retry,
											False)
		return response

	def rollbackHDCAlgo(self,algoName :str,hdcName:str
						,requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.Response:
		requestConfig.useMaster = True
		clientInfo = self.getClientInfo(graphSetName=requestConfig.graphName, useMaster=requestConfig.useMaster,
										isGlobal=True)
		arequest = ultipa_pb2.RollbackAlgoRequest(algo_name=algoName,
												   with_server=ultipa_pb2.WithServer(hdc_server_name=hdcName))
		rollbackRet = clientInfo.Controlsclient.RollbackAlgo(arequest, metadata=clientInfo.metadata)
		status = FormatType.status(rollbackRet.status)
		response = ULTIPA_RESPONSE.Response(status=status)
		if self.defaultConfig.responseWithRequestInfo:
			response.req = ULTIPA.ReturnReq(self.graphSetName, "RollbackAlgo",
											requestConfig.useHost if requestConfig.useHost else self.host,
											requestConfig.retry,
											False)
		return response

	def showHDCAlgo(self,hdcName:str
						,requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.Response:
		command=CommandList.showHDCAlgo
		commandp=f"'{hdcName}'"
		uqlMaker = UQLMAKER(command=command, commandP=commandp, commonParams=requestConfig)
		res=self.uqlSingle(uqlMaker)
		result = res.alias('_algoList_from_hdc-server-1')
		return result
