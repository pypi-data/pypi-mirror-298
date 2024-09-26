from typing import Dict, Optional

from pydantic import BaseModel

from deeploy.common.functions.functions import to_lower_camel
from deeploy.enums.inference_endpoint import InferenceEndpoint


class JobSchedule(BaseModel):
    id: str
    name: str
    cron_expression: str
    deployment: Optional[Dict]
    workspace_id: str
    endpoint: InferenceEndpoint
    active: bool
    last_run_successful: Optional[bool]
    last_run_at: Optional[str]
    created_by: str
    created_at: str
    last_updated_by: str
    updated_at: str

    class Config:
        alias_generator = to_lower_camel
