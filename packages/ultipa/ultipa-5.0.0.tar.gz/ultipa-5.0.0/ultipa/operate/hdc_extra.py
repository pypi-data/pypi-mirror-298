from typing import List, Dict

from ultipa.utils.convert import convertToGraph, convertTableToDict

from ultipa.configuration import RequestConfig

from ultipa.structs import HDCUpdateType, GraphSet
from ultipa.utils import  CommandList,UQLMAKER
from ultipa.types import ULTIPA, ULTIPA_RESPONSE
from ultipa.operate.base_extra import BaseExtra
from ultipa.structs.Schema import Schema
REPLACE_KEYS = {
	"graph": "name",
}
class HDCExtra(BaseExtra):

    def createHDCGraphBySchema(self,graphName: str,nodeSchemas: [Dict[str,List[str]]],edgeSchemas:[Dict[str,List[str]]],hdcName: str,updata: HDCUpdateType,requestConfig: RequestConfig = RequestConfig())->ULTIPA_RESPONSE.UltipaResponse:
        command=CommandList.createHDCGraph
        uqlmarker=UQLMAKER(command=command,commonParams=requestConfig)
        def getschemalist(schemas: []):
            schemalist = []
            for data in schemas:
                for key,value in data.items():
                    if key== '*':
                        schemalist.append(f'"{key}":{value}')
                    else :
                        schemalist.append(f'{key}:{value}')
            return schemalist

        nodeSchemas = ','.join(getschemalist(nodeSchemas))
        edgeSchemas = ','.join(getschemalist(edgeSchemas))
        commP = '{nodes:{%s},edges:{%s},query:"query",type:"Graph",update:"%s",default:true}' % (
        nodeSchemas, edgeSchemas,updata)

        uqlmarker.setCommandParams([graphName,commP])
        uqlmarker.addParam(key='to', value=f'{hdcName}')
        res = self.uqlSingle(uqlmarker)
        return res
    def showHDCGraph(self,requestConfig: RequestConfig = RequestConfig())->List[dict]:

        command=CommandList.showHDCGraph
        uqlmaker=UQLMAKER(command=command , commonParams=requestConfig)
        uqlmaker.setCommandParams("")
        res = self.uqlSingle(uqlmaker)

        res.data = convertTableToDict(res.alias("_projectList").data.rows,res.alias("_projectList").data.headers)
        return res.data

    def dropHDCGraph(self,graphName:str,requestConfig: RequestConfig = RequestConfig())->ULTIPA_RESPONSE.UltipaResponse:
        command=CommandList.dropHDCGraph
        uqlmaker = UQLMAKER(command=command, commonParams=requestConfig)
        uqlmaker.setCommandParams(graphName)
        res = self.uqlSingle(uqlmaker)
        return res

