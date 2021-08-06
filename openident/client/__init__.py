from datetime import datetime
import json
from uuid import UUID

from attr import attrib, attrs


@attrs(slots=True)
class Client:
    id: UUID = attrib(default=None)
    name: str = attrib(default=None)
    secret: str = attrib(default=None)
    scope: list[str] = attrib(default=None)
    redirect_uris: list[str] = attrib(default=None)
    created_at: datetime = attrib(default=None)

    def as_dict(self) -> dict:
        return {
            "id": str(self.id),
            "name": self.name,
            "secret": self.secret,
            "scope": self.scope,
            "redirect_uris": self.redirect_uris,
            "created_at": self.created_at.isoformat(),
        }

    def to_json(self) -> str:
        return json.dumps(self.as_dict(), indent=4, sort_keys=True)
