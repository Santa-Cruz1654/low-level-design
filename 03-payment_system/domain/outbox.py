from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional


@dataclass
class OutboxEvent:

    event_id: str

    event_type: str

    aggregate_id: str

    payload: dict[str, Any]

    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    published_at: Optional[datetime] = None

    attempts: int = 0