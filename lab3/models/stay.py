
import sqlalchemy as sa
from sqlalchemy import orm
from .base import myBase


class Stay(myBase):
    """Проживання: конкретний клієнт у конкретному номері за певний період."""
    __tablename__ = 'stays'

    stay_id = sa.Column(sa.Integer, sa.Identity(always=True), primary_key=True)

    client_id = sa.Column(
        sa.Integer,
        sa.ForeignKey('clients.client_id', ondelete='CASCADE', name='fk_stays_client'),
        nullable=False,
    )
    room_id = sa.Column(
        sa.Integer,
        sa.ForeignKey('rooms.room_id', name='fk_stays_room'),
        nullable=False,
    )

    checkin_date = sa.Column(sa.Date, nullable=False)
    checkout_date = sa.Column(sa.Date, nullable=True)  # NULL = ще проживає

    __table_args__ = (
        sa.CheckConstraint(
            'checkout_date IS NULL OR checkout_date >= checkin_date',
            name='ck_stays_dates',
        ),
    )

    client = orm.relationship('Client', back_populates='stays')
    room = orm.relationship('Room', back_populates='stays')

    def __repr__(self):
        return (f'<Stay(id={self.stay_id}, client_id={self.client_id}, room_id={self.room_id}, '
                f'in={self.checkin_date}, out={self.checkout_date})>')
