
import sqlalchemy as sa
from sqlalchemy import orm
from .base import myBase


class RoomType(myBase):
    """Тип номера: одномісний / двомісний / тримісний."""
    __tablename__ = 'room_types'

    room_type_id = sa.Column(sa.Integer, sa.Identity(always=True), primary_key=True)
    name = sa.Column(sa.Text, nullable=False)
    capacity = sa.Column(sa.Integer, nullable=False)
    price_per_day = sa.Column(sa.Numeric(10, 2), nullable=False)

    __table_args__ = (
        sa.UniqueConstraint('name', name='uq_room_types_name'),
        sa.CheckConstraint('capacity BETWEEN 1 AND 3', name='ck_room_types_capacity'),
        sa.CheckConstraint('price_per_day > 0', name='ck_room_types_price'),
    )

    rooms = orm.relationship('Room', back_populates='room_type')

    def __repr__(self):
        return (f'<RoomType(id={self.room_type_id}, name={self.name}, '
                f'capacity={self.capacity}, price={self.price_per_day})>')
