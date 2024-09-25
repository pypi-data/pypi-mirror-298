from pydantic import BaseModel
from typing import Callable
from uuid import UUID
from field_manager_api.config.config import DATA_URL


class Project(BaseModel):
    external_id: str
    height_reference: str
    name: str
    organization_id: UUID
    project_id: UUID
    srid: int


def get_projects_request(headers: dict, request_handler: Callable) -> list[Project]:
    """Get projects request"""
    url = f"{DATA_URL}/projects"
    return request_handler(url=url, headers=headers)
