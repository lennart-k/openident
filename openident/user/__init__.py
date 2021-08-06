from datetime import datetime
import json
from uuid import UUID

from attr import attrib, attrs


@attrs(slots=True)
class User:
    id: UUID = attrib(default=None)
    name: str = attrib(default=None)
    created_at: datetime = attrib(default=None)

    def as_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
        }

    def to_json(self) -> str:
        return json.dumps(self.as_dict(), indent=4, sort_keys=True)
