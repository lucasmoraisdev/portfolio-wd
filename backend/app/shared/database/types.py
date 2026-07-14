from typing import Annotated
from uuid import UUID, uuid4

from sqlalchemy.orm import mapped_column
from sqlalchemy import Uuid

PrimaryKey = Annotated[
    UUID,
    mapped_column(
        Uuid,
        primary_key=True,
        default=uuid4,
    )
]