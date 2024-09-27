# Copyright 2024 Agnostiq Inc.

from pydantic import ConfigDict
from pydantic.dataclasses import dataclass

from covalent_cloud import CloudExecutor

executor_plugin_name = "oci_cloud"


@dataclass(config=ConfigDict(extra="forbid"))
class OCICloudExecutor(CloudExecutor):
    """
    OCICloudExecutor is used to target BYOC infrastructure on OCI.
    """

    shape: str = "VM.Standard1.1"
