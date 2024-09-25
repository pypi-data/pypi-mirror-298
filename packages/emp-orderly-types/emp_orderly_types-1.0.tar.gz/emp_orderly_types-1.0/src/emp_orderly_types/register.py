from pydantic import BaseModel


class OrderlyRegistration(BaseModel):
    id: int
    orderly_key: str
