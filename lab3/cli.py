
import click
from queries import common
from scripts import database
from api.engine import DBConn
from models.base import myBase

# IMPORTANT: all models should be imported before the call to
#            myBase.metadata.create_all();
#            otherway no tables will be created
from models import *


@click.group()
def cli():
    # Щоб підключитися до бази, потрібно створити об'єкт engine. Зауважимо, що в цей момент програма
    # ще не підключилася до бази. Воно створило пул з'єднань, і коли бібліотеці SQLAlchemy знадобиться
    # виконати команду, вона запросить з'єднання з цього пулу.
    DBConn()


@cli.command(help='Створити таблиці в БД')
def create_tables():
    # Щоб створити логічну структуру даних, визначену в метаданих, потрібно викликати метод
    # metadata.create_all(engine).
    myBase.metadata.create_all(DBConn.engine)


@cli.command(help='Видалити таблиці в БД')
def drop_tables():
    myBase.metadata.drop_all(DBConn.engine)


@cli.command(help='Заповнити БД тестовими даними')
def fill_db():
    database.fill_db()


@cli.command(help='Запит 1: клієнти, які проживають у заданому номері')
@click.option('--room', '-r', type=click.INT, default=101, show_default=True,
              help='номер кімнати')
def room_clients(room):
    common.clients_in_room(room)


@cli.command(help='Запит 2: клієнти, які прибули із заданого міста')
@click.option('--city', '-c', default='Харків', show_default=True,
              help='місто, з якого прибув клієнт')
def city_clients(city):
    common.clients_from_city(city)


@cli.command(help='Запит 3: хто зі службовців прибирав номер клієнта у заданий день тижня')
@click.option('--passport', '-p', default='ЕК456789', show_default=True,
              help='номер паспорта клієнта')
@click.option('--weekday', '-w', type=click.IntRange(1, 7), default=3, show_default=True,
              help='день тижня: 1 - понеділок ... 7 - неділя')
def room_cleaner(passport, weekday):
    common.who_cleaned(passport, weekday)


@cli.command(help='Запит 4: чи є вільні номери та вільні місця, і скільки')
def availability():
    common.free_rooms_and_places()


@cli.command(help='Виконати всі чотири запити з прикладами параметрів')
def run_queries():
    common.run_all()


if __name__ == '__main__':
    cli()
