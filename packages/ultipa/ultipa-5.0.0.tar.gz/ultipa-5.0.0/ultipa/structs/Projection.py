from ultipa.structs.BaseModel import BaseModel

class Projection(BaseModel):

    def __init__(self,name: str,type: str,filterType: str, isDefault: str,sourceGraph: str,status: str,stats: str,hdcName: str,hdcStatus: str,config: str):
        self.name = name
        self.type = type
        self.filterType = filterType
        self.isDefault = isDefault
        self.souceGraph = sourceGraph
        self.status = status
        self.stats = stats
        self.hdcName = hdcName
        self.hdcStatus = hdcStatus
        self.config = config