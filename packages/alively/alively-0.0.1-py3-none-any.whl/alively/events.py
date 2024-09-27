import datetime as dt
from typing import Any
from pydantic import BaseModel


class dbtEventInfo(BaseModel):
    category: str
    code: str
    extra: dict[str, Any]
    invocation_id: str
    level: str
    msg: str
    name: str
    pid: int
    thread: str
    ts: dt.datetime

    def hourstamp(self) -> str:
        hour = str(self.ts.hour).zfill(2)
        minute = str(self.ts.minute).zfill(2)
        second = str(self.ts.minute).zfill(2)
        return f"{hour}:{minute}:{second}"

class dbtEvent(BaseModel):
    data: dict[str, Any]
    info: dbtEventInfo

    @property
    def name(self):
        return self.info.name