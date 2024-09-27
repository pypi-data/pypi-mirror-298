from datetime import date

from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError

from ...tools import time_now
from .models import Session, WorkInfo


def dbmutithread(func):
    def wrapper(*args, **kwargs):
        session = Session()
        rst = func(session, *args, **kwargs)
        try:
            session.commit()
            if rst == bool:
                return True
            else:
                return rst
        except IntegrityError:
            session.rollback()
            if rst == bool:
                return False
            else:
                return rst
        finally:
            session.close()

    return wrapper


@dbmutithread
def write_work_info(session, _type: int, continued: int) -> bool:
    if (
        not session.query(WorkInfo)
        .filter(WorkInfo.create_time == time_now(), WorkInfo.type == _type)
        .first()
    ):
        info = WorkInfo(type=_type, continued=continued)
        session.add(info)
    return bool


@dbmutithread
def get_last_work_info(session) -> WorkInfo:
    item = (
        session.query(WorkInfo)
        .order_by(desc(WorkInfo.create_time))
        .filter(WorkInfo.create_time.like(date + "%"), WorkInfo.type > 0)
    )
    return item
