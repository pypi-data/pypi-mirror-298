from enum import Enum
from typing import List, Literal, Optional, Union

from pydantic import BaseModel


class Protocol(str, Enum):
    FILE = "file://"
    S3 = "morph-storage://"


class SignedUrlResponse(BaseModel):
    url: str


class RefResponse(BaseModel):
    cell_type: str
    filepath: str
    alias: str
    code: Optional[str] = None
    connection_slug: Optional[str] = None


class FileCellParams(BaseModel):
    type: Literal["file"]
    filepath: Optional[str] = None
    timestamp: Optional[int] = None
    base_url: Optional[str] = None
    team_slug: Optional[str] = None
    authorization: Optional[str] = None


class SqlCellParams(BaseModel):
    type: Literal["sql"]
    sql: str
    connection_slug: Optional[str] = None
    database_id: Optional[str] = None
    base_url: Optional[str] = None
    team_slug: Optional[str] = None
    authorization: Optional[str] = None


class PythonCellParams(BaseModel):
    type: Literal["python"]
    reference: str
    timestamp: Optional[int] = None
    base_url: Optional[str] = None
    team_slug: Optional[str] = None
    authorization: Optional[str] = None


LoadDataParams = Union[RefResponse, FileCellParams, SqlCellParams]


class StorageFile(BaseModel):
    name: str
    path: str
    size: int


class StorageDirectory(BaseModel):
    name: str
    path: str
    directories: List["StorageDirectory"] = []
    files: List[StorageFile] = []


class ListStorageDirectoryResponse(BaseModel):
    path: str
    directories: List[StorageDirectory] = []
    files: List[StorageFile] = []


class MorphApiError(Exception):
    pass


class EnvVars(BaseModel):
    database_id: str
    base_url: str
    team_slug: str
    api_key: str
    canvas: Optional[str] = None
