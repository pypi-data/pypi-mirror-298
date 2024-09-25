from pydantic import BaseModel


class Location(BaseModel):
    location_id: str
    name: str
    point_easting: float
    point_northing: float
    point_z: float
    project_id: str
    srid: int
