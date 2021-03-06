# -*- coding: utf-8 -*-
# Copyright (c) 2021 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Get path to default repository or workspace."""

import os
from typing import Any, Dict

from lpot.ux.utils.exceptions import ClientErrorException
from lpot.ux.utils.templates.workdir import Workdir


def get_default_path(data: Dict[str, Any]) -> Dict[str, Any]:
    """Get paths repository or workspace."""
    workdir = Workdir()
    path = os.environ["HOME"]
    if os.path.isfile(workdir.workloads_json):
        path = workdir.get_active_workspace()
    else:
        workdir.set_active_workspace(path)

    return {"path": path}


def set_workspace(data: Dict[str, Any]) -> Dict[str, Any]:
    """Set workspace."""
    workspace_path = data.get("path", None)

    if not workspace_path:
        raise ClientErrorException("Parameter 'path' is missing in request.")

    os.makedirs(workspace_path, exist_ok=True)
    workdir = Workdir()
    workdir.set_active_workspace(workspace_path)

    return {"message": "SUCCESS"}


def get_workloads_list(data: dict) -> Dict[str, Any]:
    """Return workloads list."""
    workspace_path = os.environ["HOME"]
    if data.get("workspace_path"):
        workspace_path = os.environ["HOME"]
    workdir = Workdir(workspace_path=workspace_path)

    return workdir.map_to_response()


def delete_workload(data: dict) -> Dict[str, Any]:
    """Delete workload based on ID."""
    workdir = Workdir(workspace_path=os.environ["HOME"])
    workdir.delete_workload(data["request_id"])
    return {"message": "SUCCESS"}
