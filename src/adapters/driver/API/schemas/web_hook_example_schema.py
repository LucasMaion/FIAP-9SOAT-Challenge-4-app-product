from pydantic import BaseModel


class WebHookExampleSchema(BaseModel):
    title: str
    message: str
    user_id: int | None = None
    created_at: str
