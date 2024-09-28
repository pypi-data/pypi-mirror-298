from typing import List

from ultipa import DBType
from ultipa.operate.base_extra import BaseExtra
from ultipa.structs.Index import Index
from ultipa.structs.Job import Job
from ultipa.types import ULTIPA_REQUEST, ULTIPA, ULTIPA_RESPONSE
from ultipa.utils import UQLMAKER, CommandList
from ultipa.configuration.RequestConfig import RequestConfig
from ultipa.utils.convert import convertTableToDict, convertToIndex, convertToFullText


class IndexExtra(BaseExtra):
    '''
	Processing class that defines settings for index related operations.
	'''

    def showIndex(self,
                  requestConfig: RequestConfig = RequestConfig()) -> List[Index]:
        '''
        Show all indice.

        Args:
            requestConfig: An object of RequestConfig class

        Returns:
            List[Index]
        '''
        # if dbType != None:
        # 	command = dbType == DBType.DBNODE and CommandList.showNodeIndex or CommandList.showEdgeIndex
        # else:
        command = CommandList.showIndex
        uqlMaker = UQLMAKER(command=command, commonParams=requestConfig)
        res = self.UqlListSimple(uqlMaker=uqlMaker, isSingleOne=False)
        indexdata = convertToIndex(res=res, all=True)
        if len(indexdata) > 0:
            res.data = indexdata
        else:
            res.data = None
        return res.data

    def showNodeIndex(self, requestConfig: RequestConfig = RequestConfig()) -> List[Index]:
        '''
        Show all Node indice.

        Args:
            requestConfig: An object of RequestConfig class

        Returns:
            List[Index]
        '''
        # res=self.showIndex(dbType=DBType.DBNODE,requestConfig=requestConfig)
        command = CommandList.showNodeIndex
        uqlMaker = UQLMAKER(command=command, commonParams=requestConfig)
        res = self.UqlListSimple(uqlMaker=uqlMaker, isSingleOne=False)
        indexdata = convertToIndex(res=res, all=False, dbtype=DBType.DBNODE)
        if len(indexdata) > 0:
            res.data = indexdata
        else:
            res.data = None
        return res.data

    def showEdgeIndex(self, requestConfig: RequestConfig = RequestConfig()) -> List[Index]:
        '''
        Show all Edge indice.

        Args:
            requestConfig: An object of RequestConfig class

        Returns:
            List[Index]
        '''
        # res=self.showIndex(dbType=DBType.DBEDGE,requestConfig=requestConfig)
        command = CommandList.showEdgeIndex
        uqlMaker = UQLMAKER(command=command, commonParams=requestConfig)
        res = self.UqlListSimple(uqlMaker=uqlMaker, isSingleOne=False)
        indexdata = convertToIndex(res=res, all=False, dbtype=DBType.DBEDGE)
        if len(indexdata) > 0:
            res.data = indexdata
        else:
            res.data = None
        return res.data

    def showFulltext(self,
                     requestConfig: RequestConfig = RequestConfig()) -> List[Index]:
        '''
        Show all full-text indice.

        Args:
            requestConfig: An object of RequestConfig class
        Returns:

            List[Index]
        '''
        # if dbType != None:
        # 	command = dbType == DBType.DBNODE and CommandList.showNodeFulltext or CommandList.showEdgeFulltext
        # else:
        command = CommandList.showFulltext
        uqlMaker = UQLMAKER(command=command, commonParams=requestConfig)
        res = self.UqlListSimple(uqlMaker=uqlMaker, isSingleOne=False)
        fulltextdata = convertToFullText(res=res)
        if len(fulltextdata) > 0:
            res.data = fulltextdata
        else:
            res.data = None
        return res.data

    # def createIndex(self, dbType: DBType, propertyName: str, schemaName: str = None,
    #                 requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
    #     '''
    #     Create an index.
    #
    #     Args:
    #         dbType: The DBType of data (DBNODE or DBEDGE)
    #
    #         schemaName: The name of schema
    #
    #         property: An object of Property class
    #
    #         requestConfig: An object of RequestConfig class
    #
    #     Returns:
    #         UltipaResponse
    #     '''
    #
    #     command = dbType == DBType.DBNODE and CommandList.createNodeIndex or CommandList.createEdgeIndex
    #     # commandP = request.toString
    #     if schemaName:
    #         commandP = "@`%s`.`%s`" % (schemaName, propertyName)
    #     elif schemaName == None:
    #         commandP = "@`*`.`%s`" % (propertyName)
    #     uqlMaker = UQLMAKER(command=command, commandP=commandP, commonParams=requestConfig)
    #     res = self.uqlSingle(uqlMaker=uqlMaker)
    #     return res

    def createNodeIndex(self, source: str, indexName: str,
                        requestConfig: RequestConfig = RequestConfig()) -> Job:
        '''
		Create an index.

		Args:
			request: An object of CreateIndex class

			requestConfig: An object of RequestConfig class

		Returns:
			UltipaResponse
		'''

        command = CommandList.createNodeIndex

        uqlMaker = UQLMAKER(command=command, commonParams=requestConfig)
        source = f'{source}'
        uqlMaker.setCommandParams([source, indexName])
        res = self.uqlSingle(uqlMaker=uqlMaker)
        result = convertTableToDict(res.alias('result').data.rows, res.alias('result').data.headers)
        return Job(id=result[0].get('new_job_id'))

    def createEdgeIndex(self, source: str, indexName: str,
                        requestConfig: RequestConfig = RequestConfig()) -> Job:
        '''
		Create an index.

		Args:
			request: An object of CreateIndex class

			requestConfig: An object of RequestConfig class

		Returns:
			UltipaResponse
		'''

        command = CommandList.createEdgeIndex
        source = f'{source}'
        uqlMaker = UQLMAKER(command=command, commonParams=requestConfig)
        uqlMaker.setCommandParams([source, indexName])
        res = self.uqlSingle(uqlMaker=uqlMaker)
        result = convertTableToDict(res.alias('result').data.rows, res.alias('result').data.headers)
        return Job(id=result[0].get('new_job_id'))

    def createFulltext(self, dbType: DBType, schemaName: str, propertyName: str, fulltextName: str,
                       requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
        '''
        Create a full-text index.

        Args:
            dbType: The DBType of data (DBNODE or DBEDGE)

            schemaName: The name of schema

            property: An object of Property class

            fulltextName: Name of the fulltext index

            requestConfig: An object of RequestConfig class

        Returns:
            UltipaResponse

        '''
        command = dbType == DBType.DBNODE and CommandList.createNodeFulltext or CommandList.createEdgeFulltext
        command1 = "@`%s`.`%s`" % (schemaName, propertyName)
        commandP = [command1, fulltextName]
        uqlMaker = UQLMAKER(command=command, commonParams=requestConfig)
        uqlMaker.setCommandParams(commandP=commandP)
        res = self.uqlSingle(uqlMaker=uqlMaker)
        return res


    def createNodeFulltext(self,schemaName: str, propertyName: str, fulltextName: str,
                           rquestConfig: RequestConfig = RequestConfig()) -> List[Job]:
        '''
        Create a full-text index.

        Args:
            request: An object of CreateFulltext class

            rquestConfig: An object of RequestConfig class

        Returns:
            UltipaResponse

        '''
        command = CommandList.createNodeFulltext
        command1 = "@`%s`.`%s`" % (schemaName, propertyName)
        commandP=[command1, fulltextName]
        uqlMaker = UQLMAKER(command=command, commonParams=rquestConfig)
        uqlMaker.setCommandParams(commandP=commandP)
        res = self.uqlSingle(uqlMaker=uqlMaker)
        result = convertTableToDict(res.alias('result').data.rows, res.alias('result').data.headers)
        return [Job(id=data.get('new_job_id')) for data in result]

    def createEdgeFulltext(self,schemaName: str, propertyName: str, fulltextName: str,
                           rquestConfig: RequestConfig = RequestConfig()) -> List[Job]:
        '''
		Create a full-text index.

		Args:
			request: An object of CreateFulltext class

			rquestConfig: An object of RequestConfig class

		Returns:
			UltipaResponse

		'''
        command = CommandList.createEdgeFulltext
        command1 = "@`%s`.`%s`" % (schemaName, propertyName)
        commandP = [command1, fulltextName]
        uqlMaker = UQLMAKER(command=command, commonParams=rquestConfig)
        uqlMaker.setCommandParams(commandP=commandP)
        res = self.uqlSingle(uqlMaker=uqlMaker)
        result = convertTableToDict(res.alias('result').data.rows, res.alias('result').data.headers)
        return [Job(id=data.get('new_job_id')) for data in result]

    def dropIndex(self, dbType:DBType,indexName:str,
                  requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
        '''
		Drop an index.

		Args:
			request: An object of DropIndex class

			requestConfig: An object of RequestConfig class

		Returns:
			UltipaResponse
		'''
        command = dbType == DBType.DBNODE and CommandList.dropNodeIndex or CommandList.dropEdgeIndex
        commandP = f'"{indexName}"'

        uqlMaker = UQLMAKER(command=command, commandP=commandP, commonParams=requestConfig)
        res = self.uqlSingle(uqlMaker=uqlMaker)
        return res

    def dropFulltext(self, dbType: DBType, fulltextName: str,
                     requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
        '''
        Drop a full-text index.

        Args:
            dbType: The DBType of data (DBNODE or DBEDGE)

            fulltextName: Name of the fulltext index

            requestConfig: An object of RequestConfig class

        Returns:
            UltipaResponse
        '''

        command = dbType == DBType.DBNODE and CommandList.dropNodeFulltext or CommandList.dropEdgeFulltext
        uqlMaker = UQLMAKER(command=command, commonParams=requestConfig)
        uqlMaker.setCommandParams(fulltextName)
        res = self.uqlSingle(uqlMaker=uqlMaker)
        return res
