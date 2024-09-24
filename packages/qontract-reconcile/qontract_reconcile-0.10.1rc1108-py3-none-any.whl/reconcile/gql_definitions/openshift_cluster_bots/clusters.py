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

from reconcile.gql_definitions.fragments.ocm_environment import OCMEnvironment
from reconcile.gql_definitions.fragments.vault_secret import VaultSecret


DEFINITION = """
fragment OCMEnvironment on OpenShiftClusterManagerEnvironment_v1 {
    name
    description
    labels
    url
    accessTokenClientId
    accessTokenUrl
    accessTokenClientSecret {
        ... VaultSecret
    }
}

fragment VaultSecret on VaultSecret_v1 {
    path
    field
    version
    format
}

query OpenshiftClusterBotsQuery($name: String) {
  clusters: clusters_v1(name: $name) {
    name
    path
    serverUrl
    ocm {
      name
      environment {
        ... OCMEnvironment
      }
      orgId
      accessTokenClientId
      accessTokenUrl
      accessTokenClientSecret {
        ... VaultSecret
      }
    }
    automationToken {
      ... VaultSecret
    }
    clusterAdmin
    clusterAdminAutomationToken {
      ... VaultSecret
    }
    disable {
      integrations
    }
  }
}
"""


class ConfiguredBaseModel(BaseModel):
    class Config:
        smart_union=True
        extra=Extra.forbid


class OpenShiftClusterManagerV1(ConfiguredBaseModel):
    name: str = Field(..., alias="name")
    environment: OCMEnvironment = Field(..., alias="environment")
    org_id: str = Field(..., alias="orgId")
    access_token_client_id: Optional[str] = Field(..., alias="accessTokenClientId")
    access_token_url: Optional[str] = Field(..., alias="accessTokenUrl")
    access_token_client_secret: Optional[VaultSecret] = Field(..., alias="accessTokenClientSecret")


class DisableClusterAutomationsV1(ConfiguredBaseModel):
    integrations: Optional[list[str]] = Field(..., alias="integrations")


class ClusterV1(ConfiguredBaseModel):
    name: str = Field(..., alias="name")
    path: str = Field(..., alias="path")
    server_url: str = Field(..., alias="serverUrl")
    ocm: Optional[OpenShiftClusterManagerV1] = Field(..., alias="ocm")
    automation_token: Optional[VaultSecret] = Field(..., alias="automationToken")
    cluster_admin: Optional[bool] = Field(..., alias="clusterAdmin")
    cluster_admin_automation_token: Optional[VaultSecret] = Field(..., alias="clusterAdminAutomationToken")
    disable: Optional[DisableClusterAutomationsV1] = Field(..., alias="disable")


class OpenshiftClusterBotsQueryQueryData(ConfiguredBaseModel):
    clusters: Optional[list[ClusterV1]] = Field(..., alias="clusters")


def query(query_func: Callable, **kwargs: Any) -> OpenshiftClusterBotsQueryQueryData:
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
        OpenshiftClusterBotsQueryQueryData: queried data parsed into generated classes
    """
    raw_data: dict[Any, Any] = query_func(DEFINITION, **kwargs)
    return OpenshiftClusterBotsQueryQueryData(**raw_data)
