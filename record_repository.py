from record import Record, engine
from uuid import UUID
from sqlmodel import Session, select
class RecordRepository:

    def add(self, raw_record: dict) -> Record:
        record = Record.from_raw(raw_record)
        with Session(engine) as session:
            session.add(record)
            session.commit()
            session.refresh(record)
        return record
    
    def get_by_id(self, id: UUID) -> Record:
        with Session(engine) as session:
            return session.get(Record, id)

    def delete(self, id: UUID) -> None:
        with Session(engine) as session:
            record = session.get(Record, id)
            if record:
                session.delete(record)
                session.commit()
    def get_all(self) -> list[Record]:
        with Session(engine) as session:
            return session.exec(select(Record)).all()