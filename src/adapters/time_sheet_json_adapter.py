import datetime
from typing import List

from src.entities.models.time_sheet_entity import TimeSheet
from src.utils.utils import camelize_dict


def time_sheet_to_json(time_sheet: TimeSheet):
    return camelize_dict(time_sheet.__dict__)


def time_sheet_list_to_json(time_sheet_list: List[TimeSheet]):
    return [camelize_dict(time_sheet.__dict__) for time_sheet in time_sheet_list]


def user_records_to_json(records: List[TimeSheet], registration_number: int, worked_hours: datetime.timedelta):
    records_list = [camelize_dict(record.__dict__) for record in records]
    result = {"records": records_list,
              "workedHours": f"User {registration_number} has worked {worked_hours} on this date"}
    return result
