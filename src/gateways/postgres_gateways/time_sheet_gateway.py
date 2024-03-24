import datetime
import uuid
from typing import List, Optional
from fastapi.encoders import jsonable_encoder
from sqlalchemy import extract

from src.entities.models.time_sheet_entity import TimeSheet, time_sheet_factory
from src.external.postgresql_database import SessionLocal
from src.gateways.orm.time_sheet_orm import TimeSheets
from src.interfaces.gateways.time_sheet_gateway_interface import ITimeSheetGateway


class PostgresDBTimeSheetRepository(ITimeSheetGateway):
    @staticmethod
    def to_entity(time_sheet: TimeSheet) -> TimeSheet:
        time_sheet = time_sheet_factory(
            record_id=time_sheet.record_id,
            record_type=time_sheet.record_type,
            registration_number=time_sheet.registration_number,
            record_time=time_sheet.record_time,
            record_date=time_sheet.record_date,
        )
        return time_sheet

    def get_by_id(self, record_id: uuid.UUID) -> Optional[TimeSheet]:
        with SessionLocal() as db:
            result = db.query(TimeSheets).filter(TimeSheets.record_id == record_id).first()
        if result:
            return self.to_entity(result)
        else:
            return None

    def get_all(self) -> List[TimeSheet]:
        records = []

        with SessionLocal() as db:
            result = db.query(TimeSheets).all()

        for record in result:
            records.append(self.to_entity(record))

        return records

    def get_all_records_by_date(self, registration_number: int, date: datetime.date) -> List[TimeSheet]:
        records = []

        with SessionLocal() as db:
            result = db.query(TimeSheets).filter(TimeSheets.record_date == date,
                                                 TimeSheets.registration_number == registration_number).all()

        for record in result:
            records.append(self.to_entity(record))

        return records

    def get_all_records_by_month(self, registration_number: int, date: datetime.date) -> List[TimeSheet]:
        records = []

        with SessionLocal() as db:
            result = db.query(TimeSheets).filter(extract('month', TimeSheets.record_date) == date.month,
                                                 extract('year', TimeSheets.record_date) == date.year,
                                                 TimeSheets.registration_number == registration_number).all()

        for record in result:
            records.append(self.to_entity(record))

        return records

    def create(self, obj_in: TimeSheet) -> TimeSheet:
        obj_in_data = jsonable_encoder(obj_in, by_alias=False)
        db_obj = TimeSheets(**obj_in_data)  # type: ignore

        with SessionLocal() as db:
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)

        new_record = self.to_entity(db_obj)  # type: ignore
        return new_record

    def update(self, record_id: uuid.UUID, obj_in: TimeSheet) -> TimeSheet:
        record_in = vars(obj_in)
        with SessionLocal() as db:
            db_obj = db.query(TimeSheets).filter(TimeSheets.record_id == record_id).first()
            obj_data = jsonable_encoder(db_obj, by_alias=False)
            for field in obj_data:
                if field in record_in:
                    setattr(db_obj, field, record_in[field])
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
        updated_record = self.to_entity(db_obj)
        return updated_record

    def remove(self, record_id: uuid.UUID) -> None:
        with SessionLocal() as db:
            db_obj = db.query(TimeSheets).filter(TimeSheets.record_id == record_id).first()
            db.delete(db_obj)
            db.commit()
