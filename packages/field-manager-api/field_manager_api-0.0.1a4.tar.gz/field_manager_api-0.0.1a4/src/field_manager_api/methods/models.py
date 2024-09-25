from pydantic import BaseModel
from datetime import datetime


class Method(BaseModel):
    name: str
    description: str
    method_type: str
    return_type: str
    return_description: str
    example: str
    code: str
    created_at: datetime
    updated_at: datetime
