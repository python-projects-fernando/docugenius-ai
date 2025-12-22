from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class GeneratedDocument:
    id: Optional[int]
    user_id: int
    document_type_id: int
    file_path_or_key: str
    created_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None

    def __post_init__(self):
        if self.created_at is None:
            from datetime import datetime, timezone
            self.created_at = datetime.now(timezone.utc)