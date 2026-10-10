
import sqlalchemy as sa
from sqlalchemy import orm
from .base import myBase


class Client(myBase):
    """Клієнт готелю (особисті дані, без прив'язки до конкретного проживання)."""
    __tablename__ = 'clients'

    client_id = sa.Column(sa.Integer, sa.Identity(always=True), primary_key=True)
    passport_number = sa.Column(sa.Text, nullable=False)
    last_name = sa.Column(sa.Text, nullable=False)
    first_name = sa.Column(sa.Text, nullable=False)
    patronymic = sa.Column(sa.Text, nullable=True)
    city = sa.Column(sa.Text, nullable=False)

    __table_args__ = (
        sa.UniqueConstraint('passport_number', name='uq_clients_passport'),
    )

    # passive_deletes=True: видалення проживань при видаленні клієнта
    # робить сама БД (ON DELETE CASCADE), ORM їх не вантажить
    stays = orm.relationship(
        'Stay', back_populates='client',
        cascade='all, delete-orphan', passive_deletes=True,
    )

    def __repr__(self):
        return f'<Client(id={self.client_id}, {self.last_name} {self.first_name}, city={self.city})>'
