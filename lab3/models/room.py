
import sqlalchemy as sa
from sqlalchemy import orm
from .base import myBase


class Room(myBase):
    """Фізичний номер готелю."""
    __tablename__ = 'rooms'

    room_id = sa.Column(sa.Integer, sa.Identity(always=True), primary_key=True)
    room_number = sa.Column(sa.Integer, nullable=False)
    floor = sa.Column(sa.Integer, nullable=False)
    phone = sa.Column(sa.Text, nullable=False)

    room_type_id = sa.Column(
        sa.Integer,
        sa.ForeignKey('room_types.room_type_id', name='fk_rooms_room_type'),
        nullable=False,
    )

    __table_args__ = (
        sa.UniqueConstraint('room_number', name='uq_rooms_room_number'),
        sa.CheckConstraint('floor > 0', name='ck_rooms_floor'),
    )

    room_type = orm.relationship('RoomType', back_populates='rooms')
    stays = orm.relationship('Stay', back_populates='room')

    def __repr__(self):
        return f'<Room(number={self.room_number}, floor={self.floor}, type_id={self.room_type_id})>'
