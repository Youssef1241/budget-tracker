from record import Record
from uuid import UUID
from sqlmodel import Session, select
class RecordRepository:
    _instance = None
    def __init__(self, engine):
        self.engine = engine

    def __new__(cls, engine):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def add(self, raw_record: dict) -> Record:
        record = Record.from_raw(raw_record)
        with Session(self.engine) as session:
            session.add(record)
            session.commit()
            session.refresh(record)
        return record
    
    def delete(self, id: UUID) -> None:
        with Session(self.engine) as session:
            record = session.get(Record, id)
            if record:
                session.delete(record)
                session.commit()

    def delete_many(self, ids: list[UUID]) -> None:
        with Session(self.engine) as session:
            for id in ids:
                record = session.get(Record, id)
                if record:
                    session.delete(record)
            session.commit()

    def get_by_id(self, id: UUID) -> Record:
        with Session(self.engine) as session:
            return session.get(Record, id)

    def get_all(self) -> list[Record]:
        with Session(self.engine) as session:
            return session.exec(select(Record)).all()
            
    def get_expense_types(self) -> list[str]:
        with Session(self.engine) as session:
            statement = select(Record.expense_type).distinct()
            return session.exec(statement).all()