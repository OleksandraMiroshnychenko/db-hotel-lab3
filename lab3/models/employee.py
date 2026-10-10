
import sqlalchemy as sa
from sqlalchemy import orm
from .base import myBase


class Employee(myBase):
    """Службовець готелю, який прибирає номери."""
    __tablename__ = 'employees'

    employee_id = sa.Column(sa.Integer, sa.Identity(always=True), primary_key=True)
    last_name = sa.Column(sa.Text, nullable=False)
    first_name = sa.Column(sa.Text, nullable=False)
    patronymic = sa.Column(sa.Text, nullable=True)

    cleaning_days = orm.relationship(
        'CleaningSchedule', back_populates='employee',
        cascade='all, delete-orphan', passive_deletes=True,
    )

    def __repr__(self):
        return f'<Employee(id={self.employee_id}, {self.last_name} {self.first_name})>'
