
import click
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


if __name__ == '__main__':
    cli()
