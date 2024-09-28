from enum import Enum

from pydantic import BaseModel


class Condition(Enum):
    success = "success"
    data_unavailable = "data unavailable"
    upstream_timeout = "upstream request timed out"
    unhandled_exception = "unhandled exception"
    invalid_request = "invalid request"
    cancelled = "cancelled"
    authentication_failure = "authentication failure"


class GravyboxRequest(BaseModel):
    pass


class GravyboxResponse(BaseModel):
    success: bool
    error: str = ""
    content: dict | None = None


class LinkRequest(GravyboxRequest):
    trace_id: str


class LinkResponse(GravyboxResponse):
    pass
