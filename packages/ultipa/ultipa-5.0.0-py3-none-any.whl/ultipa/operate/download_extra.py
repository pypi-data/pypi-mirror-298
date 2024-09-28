import json
from typing import List, Callable

from ultipa import Job
from ultipa.operate.base_extra import BaseExtra
from ultipa.proto import ultipa_pb2
from ultipa.types import ULTIPA_REQUEST, ULTIPA_RESPONSE, ULTIPA
from ultipa.utils.format import FormatType
from ultipa.configuration.RequestConfig import RequestConfig
from ultipa.connection.clientType import ClientType
from ultipa.operate.task_extra import TaskExtra

class DownloadExtra(BaseExtra):
	'''
	Processing class that defines settings for file downloading operation.

	'''

	def _downloadAlgoResultFile(self, fileName: str,  cb: Callable[[bytes], None],
								requestConfig: RequestConfig = RequestConfig()):
		'''
		Download file.

		Args:
			filename: Name of the file

			taskID: id of the task

			cb: Callback function that accepts bytes

			requestConfig: An object of RequestConfig class

		Returns:
			stream
		'''
		downResponse = ULTIPA_RESPONSE.Response()
		try:

			clientInfo = self.getClientInfo(graphSetName=requestConfig.graphName, useMaster=requestConfig.useMaster,
											clientType=ClientType.Leader)
			res = clientInfo.Controlsclient.DownloadFile(
				ultipa_pb2.DownloadFileRequest(file_name=fileName), metadata=clientInfo.metadata)

			for data_flow in res:
				ultipa_response = ULTIPA_RESPONSE.Response()
				status = FormatType.status(data_flow.status)
				ultipa_response.status = status
				if status.code != ULTIPA.Code.SUCCESS:
					cb(ultipa_response)
					break
				ultipa_response.data = data_flow.chunk
				cb(ultipa_response.data)
		except Exception as e:
			downResponse.status = ULTIPA.Status(code=ULTIPA.Code.UNKNOW_ERROR, message=str(e))
			print(downResponse.status.message)

	def downloadAlgoResultFile(self, fileName: str,  cb: Callable[[bytes], None],jobId: str=None,
							   requestConfig: RequestConfig = RequestConfig()):
		'''
		Download file.

		Args:
			filename: Name of the file

			taskID: id of the task

			cb:Callback function that accepts bytes

			requestConfig: An object of RequestConfig class

		Returns:
			stream
		'''
		result=TaskExtra.showJob(self,jobId=jobId)
		if result:
			for data in result:
				if data.id == str(jobId):
					for key,value in json.loads(data.result).items():
						if value.split(r'/')[-1] == fileName:
							return self._downloadAlgoResultFile(fileName=value, cb=cb, requestConfig=requestConfig)


		else :
			return Job(id='',error='Job not found')
		return Job(id='',error='file not found')

	def _downloadAllAlgoResultFile(self, fileName: str,  cb: Callable[[bytes, str], None],
								   requestConfig: RequestConfig = RequestConfig()):
		'''
		Download all files.

		Args:
			filename: Name of the file

			taskID: id of the task

			cb: Callback function that accepts bytes and string inputs

			requestConfig: An object of RequestConfig class

		Returns:
			stream
		'''
		downResponse = ULTIPA_RESPONSE.Response()
		try:

			clientInfo = self.getClientInfo(graphSetName=requestConfig.graphName, useMaster=requestConfig.useMaster,
											clientType=ClientType.Leader)
			res = clientInfo.Controlsclient.DownloadFile(
				ultipa_pb2.DownloadFileRequest(file_name=fileName), metadata=clientInfo.metadata)

			for data_flow in res:
				ultipa_response = ULTIPA_RESPONSE.Response()
				status = FormatType.status(data_flow.status)
				ultipa_response.status = status
				if status.code != ULTIPA.Code.SUCCESS:
					cb(ultipa_response)
					break
				ultipa_response.data = data_flow.chunk
				cb(ultipa_response.data, fileName)
		except Exception as e:
			downResponse.status = ULTIPA.Status(code=ULTIPA.Code.UNKNOW_ERROR, message=str(e))
			print(downResponse.status.message)

	def downloadAllAlgoResultFile(self, cb: Callable[[bytes, str], None],jobId: str=None,
								  requestConfig: RequestConfig = RequestConfig()):
		'''
		Download all files.

		Args:

			taskID: id of the task

			cb: callback function for receiving data

			requestConfig: An object of RequestConfig class

		Returns:
			stream
		'''
		result = TaskExtra.showJob(self, jobId=jobId)
		filename = []
		if result:
			for data in result:
				if data.id == str(jobId):
					for key,value in json.loads(data.result).items():
						if key[:11] == 'output_file':
							filename.append(value)

		else:
			raise Exception('Job not found')

		for name in filename:
			self._downloadAllAlgoResultFile(fileName=name, cb=cb, requestConfig=requestConfig)
