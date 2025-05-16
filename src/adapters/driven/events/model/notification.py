from datetime import datetime
from pydantic import BaseModel


class Notification(BaseModel):
    title: str
    message: str  # Can use stringification for more complex objects
    user_id: int | None = None
    created_at: datetime = datetime.now()
