
import sqlalchemy as sa
from sqlalchemy import orm
from .base import myBase


class CleaningSchedule(myBase):
    """Графік прибирання: який поверх службовець прибирає в певний день тижня."""
    __tablename__ = 'cleaning_schedule'

    employee_id = sa.Column(
        sa.Integer,
        sa.ForeignKey('employees.employee_id', ondelete='CASCADE',
                      name='fk_cleaning_schedule_employee'),
        nullable=False,
    )
    weekday = sa.Column(sa.SmallInteger, nullable=False)  # 1=Пн ... 7=Нд
    floor = sa.Column(sa.Integer, nullable=False)

    __table_args__ = (
        # складений первинний ключ: один поверх на пару "службовець + день"
        sa.PrimaryKeyConstraint('employee_id', 'weekday', name='pk_cleaning_schedule'),
        sa.CheckConstraint('weekday BETWEEN 1 AND 7', name='ck_cleaning_schedule_weekday'),
        sa.CheckConstraint('floor > 0', name='ck_cleaning_schedule_floor'),
    )

    employee = orm.relationship('Employee', back_populates='cleaning_days')

    def __repr__(self):
        return f'<CleaningSchedule(employee_id={self.employee_id}, weekday={self.weekday}, floor={self.floor})>'
