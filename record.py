from uuid import UUID,uuid4
from datetime import datetime
from sqlmodel import SQLModel, Field, create_engine

class Record(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    date_time: datetime = Field(default_factory=lambda: datetime.now())
    name: str
    value: float
    expense_type: str

    @classmethod
    def from_raw(cls, raw_data: dict)-> "Record":
        return cls(**raw_data)

