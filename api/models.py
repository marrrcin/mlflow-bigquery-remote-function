# BigQuery requests look like this:
# {
#  "requestId": "124ab1c",
#  "caller": "//bigquery.googleapis.com/projects/myproject/jobs/myproject:US.bquxjob_5b4c112c_17961fafeaf",
#  "sessionUser": "test-user@test-company.com",
#  "userDefinedContext": {
#   "key1": "value1",
#   "key2": "v2"
#  },
#  "calls": [
#   [null, 1, "", "abc"],
#   ["abc", "9007199254740993", null, null]
#  ]
# }
from dataclasses import dataclass
from typing import Dict, List, Any, Optional

from pydantic import BaseModel


@dataclass
class AppContext:
    model: Any = None


class BigQueryUDFRequest(BaseModel):
    request_id: Optional[str]
    caller: str
    sessionUser: str
    userDefinedContext: Optional[Dict]
    calls: List[List[Any]] = []


class BigQueryUDFResponse(BaseModel):
    replies: List[Any]
