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
query Maintenances {
  maintenances: maintenance_v1 {
    name
    message
    scheduledStart
    scheduledEnd
    affectedServices {
      name
    }
    announcements {
      provider
      ... on MaintenanceStatuspageAnnouncement_v1 {
        page {
          name
        }
        remindSubscribers
        notifySubscribersOnStart
        notifySubscribersOnCompletion
      }
    }
  }
}
"""


class ConfiguredBaseModel(BaseModel):
    class Config:
        smart_union=True
        extra=Extra.forbid


class AppV1(ConfiguredBaseModel):
    name: str = Field(..., alias="name")


class MaintenanceAnnouncementV1(ConfiguredBaseModel):
    provider: str = Field(..., alias="provider")


class StatusPageV1(ConfiguredBaseModel):
    name: str = Field(..., alias="name")


class MaintenanceStatuspageAnnouncementV1(MaintenanceAnnouncementV1):
    page: StatusPageV1 = Field(..., alias="page")
    remind_subscribers: Optional[bool] = Field(..., alias="remindSubscribers")
    notify_subscribers_on_start: Optional[bool] = Field(..., alias="notifySubscribersOnStart")
    notify_subscribers_on_completion: Optional[bool] = Field(..., alias="notifySubscribersOnCompletion")


class MaintenanceV1(ConfiguredBaseModel):
    name: str = Field(..., alias="name")
    message: str = Field(..., alias="message")
    scheduled_start: str = Field(..., alias="scheduledStart")
    scheduled_end: str = Field(..., alias="scheduledEnd")
    affected_services: list[AppV1] = Field(..., alias="affectedServices")
    announcements: Optional[list[Union[MaintenanceStatuspageAnnouncementV1, MaintenanceAnnouncementV1]]] = Field(..., alias="announcements")


class MaintenancesQueryData(ConfiguredBaseModel):
    maintenances: Optional[list[MaintenanceV1]] = Field(..., alias="maintenances")


def query(query_func: Callable, **kwargs: Any) -> MaintenancesQueryData:
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
        MaintenancesQueryData: queried data parsed into generated classes
    """
    raw_data: dict[Any, Any] = query_func(DEFINITION, **kwargs)
    return MaintenancesQueryData(**raw_data)
