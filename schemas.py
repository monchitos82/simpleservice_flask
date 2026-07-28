from typing import Optional

from pydantic import BaseModel, ConfigDict
from datetime import datetime

class RequestLogSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True) 
    
    id: Optional[int] = None
    ip_address: str
    endpoint: str
    method: str
    response_code: int
    timestamp: datetime
    scheme: str | None