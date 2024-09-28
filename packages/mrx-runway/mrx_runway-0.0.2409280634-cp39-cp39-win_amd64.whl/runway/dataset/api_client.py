#
#  MAKINAROCKS CONFIDENTIAL
#  ________________________
#
#  [2017] - [2024] MakinaRocks Co., Ltd.
#  All Rights Reserved.
#
#  NOTICE:  All information contained herein is, and remains
#  the property of MakinaRocks Co., Ltd. and its suppliers, if any.
#  The intellectual and technical concepts contained herein are
#  proprietary to MakinaRocks Co., Ltd. and its suppliers and may be
#  covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law. Dissemination
#  of this information or reproduction of this material is
#  strictly forbidden unless prior written permission is obtained
#  from MakinaRocks Co., Ltd.
from typing import Any, BinaryIO, Dict, Final, Optional

import requests
from pydantic import BaseModel

from runway.common.utils import exception_handler, exclude_none
from runway.model_registry.values import WorkloadType

# NOTE module-hierarchy 가 맞지 않기 때문에 rev2 보다 큰 revision 이 생성되면 수정되어야 한다.
from runway.settings import settings

REQUEST_TIMEOUT: Final[int] = 10


def upload_data_snapshot_and_version(
    name: str,
    binary: BinaryIO,
    description: Optional[str] = None,
) -> dict:
    if settings.launch_params is None or settings.launch_params.source is None:
        raise ValueError("There are no launch parameters")

    if description is not None and len(description) > 100:
        raise ValueError("Description must be less than 100 characters")

    # TODO 나중에는 참조하는 코드가 없어야 한다...
    if settings.launch_params.source.entityname == WorkloadType.dev_instance:
        response = exception_handler(
            requests.post(
                (
                    f"http://{settings.RUNWAY_API_SERVER_URL}"
                    f"/v1/link/workspaces/{settings.RUNWAY_WORKSPACE_ID}"
                    f"/projects/{settings.RUNWAY_PROJECT_ID}"
                    "/data-snapshots/sdk"
                ),
                headers={"Authorization": f"Bearer {settings.TOKEN}"},
                files={"file": binary},
                data=exclude_none(
                    {
                        "name": name,
                        "description": description,
                    },
                ),
                timeout=REQUEST_TIMEOUT,
            ),
        )

        return response.json()
    elif settings.launch_params.source.entityname == WorkloadType.pipeline:
        response = exception_handler(
            requests.post(
                (
                    f"http://{settings.RUNWAY_API_SERVER_URL}"
                    "/v1/internal/workspaces/projects"
                    f"/{settings.RUNWAY_PROJECT_ID}/data-snapshots/sdk"
                ),
                files={"file": binary},
                data=exclude_none(
                    {
                        "user_id": settings.RUNWAY_USER_ID,
                        "name": name,
                        "description": description,
                        "argo_workflow_run_id": settings.ARGO_WORKFLOW_RUN_ID,
                    },
                ),
                timeout=REQUEST_TIMEOUT,
            ),
        )

        return response.json()
    else:
        raise ValueError(
            "entity name of launch parameters should be in [dev_instance, pipeline]",
        )


def create_data_snapshot(
    name: str,
    description: Optional[str] = None,
    exist_ok: bool = False,
) -> dict:
    if settings.launch_params is None or settings.launch_params.source is None:
        raise ValueError("There are no launch parameters")

    if description is not None and len(description) > 100:
        raise ValueError("Description must be less than 100 characters")

    # TODO 나중에는 참조하는 코드가 없어야 한다...
    if settings.launch_params.source.entityname == WorkloadType.dev_instance:
        response = exception_handler(
            requests.post(
                (
                    f"http://{settings.RUNWAY_API_SERVER_URL}"
                    f"/v1/link/workspaces/{settings.RUNWAY_WORKSPACE_ID}"
                    f"/projects/{settings.RUNWAY_PROJECT_ID}"
                    f"/data-snapshots"
                ),
                headers={"Authorization": f"Bearer {settings.TOKEN}"},
                data=exclude_none(
                    {
                        "name": name,
                        "description": description,
                        "exist_ok": exist_ok,
                    },
                ),
                timeout=REQUEST_TIMEOUT,
            ),
        )

        return response.json()
    elif settings.launch_params.source.entityname == WorkloadType.pipeline:
        response = exception_handler(
            requests.post(
                (
                    f"http://{settings.RUNWAY_API_SERVER_URL}"
                    "/v1/internal/workspaces/projects"
                    f"/{settings.RUNWAY_PROJECT_ID}/data-snapshots"
                ),
                data=exclude_none(
                    {
                        "user_id": settings.RUNWAY_USER_ID,
                        "name": name,
                        "description": description,
                        "exist_ok": exist_ok,
                    },
                ),
                timeout=REQUEST_TIMEOUT,
            ),
        )

        return response.json()
    else:
        raise ValueError(
            "entity name of launch parameters should be in [dev_instance, pipeline]",
        )


def create_data_snapshot_version(
    dataset_name: str,
    description: Optional[str] = None,
) -> dict:
    if settings.launch_params is None or settings.launch_params.source is None:
        raise ValueError("There are no launch parameters")

    if description is not None and len(description) > 100:
        raise ValueError("Description must be less than 100 characters")

    # TODO 나중에는 참조하는 코드가 없어야 한다...
    if settings.launch_params.source.entityname == WorkloadType.dev_instance:
        # Find data_snapshot_id using dataset_name
        response = exception_handler(
            requests.get(
                (
                    f"http://{settings.RUNWAY_API_SERVER_URL}"
                    f"/v1/link/workspaces/{settings.RUNWAY_WORKSPACE_ID}"
                    f"/projects/{settings.RUNWAY_PROJECT_ID}"
                    f"/data-snapshots/name?name={dataset_name}"
                ),
                headers={
                    "Authorization": f"Bearer {settings.TOKEN}",
                },
                timeout=REQUEST_TIMEOUT,
            ),
        )
        data_snapshot = response.json().get("data_snapshot", None)
        if data_snapshot is None:
            raise ValueError(f"Dataset '{dataset_name}' does not exist.")
        data_snapshot_id = data_snapshot.get("id", None)
        if data_snapshot_id is None:
            raise ValueError("Data snapshot id does not exist.")

        # Upgrade dataset version
        response = exception_handler(
            requests.post(
                (
                    f"http://{settings.RUNWAY_API_SERVER_URL}"
                    f"/v1/link/workspaces/{settings.RUNWAY_WORKSPACE_ID}"
                    f"/projects/{settings.RUNWAY_PROJECT_ID}"
                    f"/data-snapshots/{data_snapshot_id}/versions"
                ),
                headers={
                    "Authorization": f"Bearer {settings.TOKEN}",
                },
                data=exclude_none({"description": description}),
                timeout=REQUEST_TIMEOUT,
            ),
        )

        return response.json()
    elif settings.launch_params.source.entityname == WorkloadType.pipeline:
        # Find data_snapshot_id using dataset_name
        response = exception_handler(
            requests.get(
                (
                    f"http://{settings.RUNWAY_API_SERVER_URL}"
                    f"/v1/internal/workspaces/projects/{settings.RUNWAY_PROJECT_ID}"
                    f"/data-snapshots/name?name={dataset_name}&user_id={settings.RUNWAY_USER_ID}"
                ),
                timeout=REQUEST_TIMEOUT,
            ),
        )

        data_snapshot = response.json().get("data_snapshot", None)
        if data_snapshot is None:
            raise ValueError(f"Dataset '{dataset_name}' does not exist.")
        data_snapshot_id = data_snapshot.get("id", None)
        if data_snapshot_id is None:
            raise ValueError("Data snapshot id does not exist.")

        # Upgrade dataset version
        response = requests.post(
            (
                f"http://{settings.RUNWAY_API_SERVER_URL}"
                f"/v1/internal/workspaces/projects/{settings.RUNWAY_PROJECT_ID}"
                f"/data-snapshots/{data_snapshot_id}/versions"
            ),
            data=exclude_none(
                {
                    "user_id": settings.RUNWAY_USER_ID,
                    "description": description,
                    "argo_workflow_run_id": settings.ARGO_WORKFLOW_RUN_ID,
                },
            ),
            timeout=REQUEST_TIMEOUT,
        )

        return response.json()
    else:
        raise ValueError(
            "entity name of launch parameters should be in [dev_instance, pipeline]",
        )
