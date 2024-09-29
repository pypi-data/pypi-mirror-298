from uuid import UUID

from pydantic import BaseModel


class OrderCreationMessage(BaseModel):
    order_id: UUID
