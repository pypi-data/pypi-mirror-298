"""
Generated by qenerate plugin=pydantic_v1. DO NOT MODIFY MANUALLY!
"""
from collections.abc import Callable  # noqa: F401 # pylint: disable=W0611
from datetime import datetime  # noqa: F401 # pylint: disable=W0611
from enum import Enum  # noqa: F401 # pylint: disable=W0611
from typing import (  # noqa: F401 # pylint: disable=W0611
    Any,
    Optional,
    Union,
)

from pydantic import (  # noqa: F401 # pylint: disable=W0611
    BaseModel,
    Extra,
    Field,
    Json,
)


DEFINITION = """
query Apps {
  apps: apps_v1 {
    path
    name
    parentApp {
      path
      name
    }
  }
}
"""


class ConfiguredBaseModel(BaseModel):
    class Config:
        smart_union=True
        extra=Extra.forbid


class AppV1_AppV1(ConfiguredBaseModel):
    path: str = Field(..., alias="path")
    name: str = Field(..., alias="name")


class AppV1(ConfiguredBaseModel):
    path: str = Field(..., alias="path")
    name: str = Field(..., alias="name")
    parent_app: Optional[AppV1_AppV1] = Field(..., alias="parentApp")


class AppsQueryData(ConfiguredBaseModel):
    apps: Optional[list[AppV1]] = Field(..., alias="apps")


def query(query_func: Callable, **kwargs: Any) -> AppsQueryData:
    """
    This is a convenience function which queries and parses the data into
    concrete types. It should be compatible with most GQL clients.
    You do not have to use it to consume the generated data classes.
    Alternatively, you can also mime and alternate the behavior
    of this function in the caller.

    Parameters:
        query_func (Callable): Function which queries your GQL Server
        kwargs: optional arguments that will be passed to the query function

    Returns:
        AppsQueryData: queried data parsed into generated classes
    """
    raw_data: dict[Any, Any] = query_func(DEFINITION, **kwargs)
    return AppsQueryData(**raw_data)
