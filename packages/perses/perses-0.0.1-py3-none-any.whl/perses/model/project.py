from typing import Literal

from perses.model.common import BaseModel, ObjectMetadata


class Project(BaseModel):
    kind: Literal["Project"] = "Project"
    metadata: ObjectMetadata
