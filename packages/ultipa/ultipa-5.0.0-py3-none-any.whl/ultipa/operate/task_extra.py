from typing import List, Optional, Union

from ultipa.types.types_response import Task

from ultipa.types.types import TaskStatus

from ultipa.configuration.RequestConfig import RequestConfig
from ultipa.operate.base_extra import BaseExtra
from ultipa.types import ULTIPA_REQUEST, ULTIPA, ULTIPA_RESPONSE
from ultipa.utils import UQLMAKER, CommandList
from ultipa.structs.Job import Job
import json

from ultipa.utils.convert import convertToAnyObject, convertToTop, convertTableToDict
from ultipa.utils.ResposeFormat import ResponseKeyFormat
from ultipa.structs.Top import Top


class ALGO_RETURN_TYPE:
    ALGO_RETURN_REALTIME = 1
    ALGO_RETURN_WRITE_BACK = 2
    ALGO_RETURN_VISUALIZATION = 4


class TaskExtra(BaseExtra):
    '''
	Processing class that defines settings for task and process related operations.
	'''

    def top(self,
            requestConfig: RequestConfig = RequestConfig()) -> List[Top]:
        '''
        Top real-time processes.

        Args:
            requestConfig: An object of RequestConfig class

        Returns:
            List[Top]

        '''
        uqlMaker = UQLMAKER(command=CommandList.top, commonParams=requestConfig)
        res = self.UqlListSimple(uqlMaker)
        if len(res.data) > 0:
            res.data = convertToTop(res)
        else:
            res.data = None
        return res.data

    def kill(self, processId: str = None, all: bool = False,
             requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
        '''
        Kill real-time processes.

        Args:
            id: The ID of real-time process

            all: Whether to kill all real-time processes

            requestConfig: An object of RequestConfig class

        Returns:
            Response

        '''
        commonP = []
        if processId:
            commonP = processId
        if all:
            commonP = '*'
        uqlMaker = UQLMAKER(command=CommandList.kill, commonParams=requestConfig)
        uqlMaker.setCommandParams(commonP)
        res = self.uqlSingle(uqlMaker)
        return res

    def license(self, requestConfig: RequestConfig = RequestConfig()):
        commond = CommandList.licenseDump
        commonP = ''
        uqlMaker = UQLMAKER(command=commond, commonParams=requestConfig)
        uqlMaker.setCommandParams(commonP)
        res = self.uqlSingle(uqlMaker)
        licensedata = convertTableToDict(res.alias('license').data.rows, res.alias('license').data.headers)
        return licensedata

    def showJob(self, jobId: str = None,
                requestConfig: RequestConfig = RequestConfig()) -> List[Job]:
        '''
		Show back-end tasks.

		Args:
			request:  An object of ShowTask class

			requestConfig: An object of RequestConfig class

		Returns:
			ResponseListTask

		'''

        _jsonKeys = ['taskJson']
        uqlMaker = UQLMAKER(command=CommandList.showJob, commonParams=requestConfig)
        if jobId:
            commonP = jobId
            uqlMaker.setCommandParams(commandP=commonP)

        res = self.UqlListSimple(uqlMaker=uqlMaker, responseKeyFormat=ResponseKeyFormat(jsonKeys=_jsonKeys))
        newDatas = []
        if res.data:
            for obj in res.data:
                obj = obj.__dict__
                newDatas.append(
                    Job(id=obj.get('job_id'), graph=obj.get('graph_name'), type=obj.get('type'), uql=obj.get('uql'),
                        gql=obj.get('gql'), status=obj.get('status'), error=obj.get('err_msg'),
                        result=obj.get('result'), startTime=obj.get('start_time'),
                        endTime=obj.get('end_time'), progress=obj.get('progress')))

            res.data = newDatas
        return res.data

    def clearJob(self, jobId: str,
                 requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
        '''
		Clear back-end tasks.

		Args:
			request:  An object of ClearTask class

			requestConfig: An object of RequestConfig class

		Returns:
			ResponseCommon

		'''

        uqlMaker = UQLMAKER(command=CommandList.clearJob, commonParams=requestConfig)
        if jobId:
            commonP = jobId
            uqlMaker.setCommandParams(commandP=commonP)

        res = self.UqlUpdateSimple(uqlMaker)

        return res

    def stopJob(self, jobId: str,
                 requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseCommon:
        '''
		Stop back-end tasks.

		Args:
			id: The ID of back-end task

			all: Whether to stop all back-end tasks that are computing

			requestConfig: An object of RequestConfig class

		Returns:
			ResponseCommon

		'''
        uqlMaker = UQLMAKER(command=CommandList.stopJob, commonParams=requestConfig)
        if jobId:
            commonP = jobId
        uqlMaker.setCommandParams(commandP=commonP)
        return self.UqlUpdateSimple(uqlMaker)

    def clusterInfo(self,
                    requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ClusterInfo:
        '''
		Show cluster information.

		Args:
			requestConfig: An object of RequestConfig class

		Returns:
			ClusterInfo

		'''
        self.refreshRaftLeader(redirectHost='', requestConfig=requestConfig)
        result = []
        if not requestConfig.graphName:
            graphSetName = 'default'
        else:
            graphSetName = requestConfig.graphName
        for peer in self.hostManagerControl.getAllHostStatusInfo(graphSetName):
            info = ULTIPA_RESPONSE.Cluster()
            info.status = peer.status
            info.host = peer.host
            info.isLeader = peer.isLeader
            info.isFollowerReadable = peer.isFollowerReadable
            info.isAlgoExecutable = peer.isAlgoExecutable
            info.isUnset = peer.isUnset
            info.cpuUsage = None
            info.memUsage = None
            if peer.status:
                ret = self.stats(requestConfig=RequestConfig(host=peer.host))
                if ret.status.code == ULTIPA.Code.SUCCESS:
                    info.cpuUsage = ret.data.cpuUsage
                    info.memUsage = ret.data.memUsage

            result.append(info)
        res = ULTIPA_RESPONSE.Response()
        res.data = result
        return res

    def showTask(self, algoNameOrId: Optional[Union[int, str]] = None, status: TaskStatus = None,
                 config: RequestConfig = RequestConfig()) -> List[Task]:
        '''
        Show back-end tasks.

        Args:

            algoNameOrld (str): The name of the task algo to show

            status (str): The status of the tasks to retrieve.

            config (RequestConfig): An object of RequestConfig class.

        Returns:
            List[Task]

        '''

        _jsonKeys = ['taskJson']
        uqlMaker = UQLMAKER(command=CommandList.showTask, commonParams=config)
        commonP = []

        # if all:
        # 	commonP.append('*')

        # else:

        if isinstance(algoNameOrId, str) or algoNameOrId is None:
            if algoNameOrId and status:
                commonP.append(algoNameOrId)
                commonP.append(status.value)
            if algoNameOrId and not status:
                commonP.append(algoNameOrId)
                commonP.append('*')
            if not algoNameOrId and status:
                commonP.append('*')
                commonP.append(status.value)

        elif isinstance(algoNameOrId, int):
            commonP = algoNameOrId

        uqlMaker.setCommandParams(commandP=commonP)
        res = self.UqlListSimple(uqlMaker=uqlMaker, responseKeyFormat=ResponseKeyFormat(jsonKeys=_jsonKeys))
        newDatas = []
        if res.data:
            for obj in res.data:
                obj = obj.__dict__
                newData = ULTIPA_RESPONSE.Task()
                taskJson = obj.get("taskJson", {})
                newData.param = json.loads(taskJson.get("param", "{}"))
                newData.result = taskJson.get("result")
                task_info = taskJson.get("task_info", {})

                if task_info.get('status_code'):
                    task_info["status_code"] = ULTIPA.TaskStatusString[task_info.get("TASK_STATUS")]
                if task_info.get('engine_cost'):
                    task_info["engine_cost"] = task_info.get("writing_start_time", 0) - task_info.get("start_time", 0)

                newData.task_info = convertToAnyObject(task_info)
                return_type_get = int(task_info.get('return_type', 0))
                return_type = ULTIPA_RESPONSE.Return_Type()
                return_type.is_realtime = True if return_type_get & ALGO_RETURN_TYPE.ALGO_RETURN_REALTIME else False
                return_type.is_visualization = True if return_type_get & ALGO_RETURN_TYPE.ALGO_RETURN_VISUALIZATION else False
                return_type.is_wirte_back = True if return_type_get & ALGO_RETURN_TYPE.ALGO_RETURN_WRITE_BACK else False
                newData.task_info.__setattr__('return_type', return_type)
                newDatas.append(newData)
            res.data = newDatas
        else:
            res.data = None
        return res.data
