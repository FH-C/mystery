from datetime import date, timedelta
from typing import List, Any
from sqlalchemy.orm import Session

from crud.base import CRUDBase
from model import SessionLocal
from model.customer import Customer


class CRUDCustomer(CRUDBase):
    def create(self, db: Session, obj_in: dict) -> Any:
        # obj_in_data = jsonable_encoder(obj_in)
        obj_in['daily_got_mark'] = {}
        for i in range(0, obj_in['days']):
            obj_in['daily_got_mark'][str(date.today() + timedelta(days=i))] = 0
        db_obj = self.model(**obj_in)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def add_got_mark(self, db: Session, id: int):
        db_obj: Customer = self.get(db, id)
        db_obj.got_mark += 1
        db_obj.real_total_mark += 1
        d = str(date.today())
        db_obj.daily_got_mark[d] -= 1
        db.commit()
        db.refresh(db_obj)
        return True

    def minus_got_mark(self, db: Session, id: int):
        db_obj: Customer = self.get(db, id)
        db_obj.got_mark -= 1
        db_obj.real_total_mark -= 1
        d = str(date.today())
        db_obj.daily_got_mark[d] -= 1
        db.commit()
        db.refresh(db_obj)
        return True
    
    def set_real_accuracy(self, db: Session, id: int, accuracy: float):
        db_obj: Customer = self.get(db, id)
        db_obj.real_accuracy = accuracy
        db.commit()
        db.refresh(db_obj)
        return True

    def get_got_mark(self, db: Session, id: int) -> int:
        db_obj: Customer = self.get(db, id)
        return db_obj.got_mark

    def get_by_url_subject_id(self, db: Session, url: str, subject_id: int, user_id: int):
        return db.query(self.model).filter(
            self.model.url == url,
            self.model.subject_id == subject_id,
            self.model.user_id == user_id
        ).first()

    def set_days(self, db: Session):
        lst = db.query(self.model).filter(
            self.model.days == 1,
            self.model.create_at >= 1668315600,
            self.model.create_at < 1668355200
        ).all()
        return lst


customer_crud = CRUDCustomer(Customer)
