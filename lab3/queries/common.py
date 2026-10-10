
from sqlalchemy import select, func, and_

from api.engine import DBConn
from models.room_type import RoomType
from models.room import Room
from models.client import Client
from models.stay import Stay
from models.employee import Employee
from models.cleaning_schedule import CleaningSchedule

WEEKDAYS = {1: 'понеділок', 2: 'вівторок', 3: 'середа', 4: 'четвер',
            5: "п'ятниця", 6: 'субота', 7: 'неділя'}


def _full_name(person):
    parts = (person.last_name, person.first_name, person.patronymic)
    return ' '.join(p for p in parts if p)


def _print_table(title, headers, rows):
    """Виводить результат у консоль у вигляді вирівняної таблиці."""
    print()
    print(title)
    if not rows:
        print('  (нічого не знайдено)')
        return
    table = [list(headers)] + [[str(v) for v in row] for row in rows]
    widths = [max(len(line[i]) for line in table) for i in range(len(headers))]
    fmt = '  '.join('{:<%d}' % w for w in widths)
    print(fmt.format(*headers))
    print('  '.join('-' * w for w in widths))
    for line in table[1:]:
        print(fmt.format(*line))


# ---------------------------------------------------------------------------
# Запит 1. Клієнти, які проживають у заданому номері
# ---------------------------------------------------------------------------
def clients_in_room(room_number):
    with DBConn.get_session() as session:
        # join(Client.stays) і join(Stay.room) - з'єднання через relationship з моделей,
        # тому умови з'єднання (ON ...) вказувати не потрібно.
        stmt = (
            select(Client, Stay.checkin_date)
            .join(Client.stays)
            .join(Stay.room)
            .where(Room.room_number == room_number,
                   Stay.checkout_date.is_(None))      # None -> IS NULL: клієнт ще живе
            .order_by(Client.last_name)
        )
        rows = [(_full_name(c), c.passport_number, checkin)
                for c, checkin in session.execute(stmt)]

    _print_table(f'Запит 1. Клієнти, які проживають у номері {room_number}:',
                 ['ПІБ', 'Паспорт', 'Дата поселення'], rows)


# ---------------------------------------------------------------------------
# Запит 2. Клієнти, які прибули із заданого міста
# ---------------------------------------------------------------------------
def clients_from_city(city):
    with DBConn.get_session() as session:
        stmt = select(Client).where(Client.city == city).order_by(Client.last_name)
        rows = [(_full_name(c), c.passport_number, c.city)
                for c in session.scalars(stmt)]

    _print_table(f'Запит 2. Клієнти, які прибули з міста {city}:',
                 ['ПІБ', 'Паспорт', 'Місто'], rows)


# ---------------------------------------------------------------------------
# Запит 3. Хто зі службовців прибирав номер вказаного клієнта у заданий день тижня
# ---------------------------------------------------------------------------
def who_cleaned(passport_number, weekday):
    with DBConn.get_session() as session:
        client = session.scalar(
            select(Client).where(Client.passport_number == passport_number))
        if client is None:
            print(f'\nЗапит 3. Клієнта з паспортом {passport_number} не знайдено.')
            return

        # Клієнт -> проживання -> номер -> (той самий поверх) -> графік -> службовець.
        # Прямого зв'язку між номером і графіком немає, вони збігаються за поверхом,
        # тому ця умова з'єднання записана явно.
        stmt = (
            select(Employee, CleaningSchedule.floor, Room.room_number)
            .select_from(Client)
            .join(Client.stays)
            .join(Stay.room)
            .join(CleaningSchedule, CleaningSchedule.floor == Room.floor)
            .join(Employee, Employee.employee_id == CleaningSchedule.employee_id)
            .where(Client.passport_number == passport_number,
                   CleaningSchedule.weekday == weekday,
                   Stay.checkout_date.is_(None))      # номер, у якому клієнт живе зараз
            .distinct()
        )
        rows = [(_full_name(e), floor, room_number)
                for e, floor, room_number in session.execute(stmt)]
        client_name = _full_name(client)

    _print_table(
        f'Запит 3. Хто прибирав номер клієнта {client_name} '
        f'({WEEKDAYS[weekday]}, день тижня {weekday}):',
        ['Службовець', 'Поверх', 'Номер клієнта'], rows)


# ---------------------------------------------------------------------------
# Запит 4. Чи є вільні номери та вільні місця, і скільки
# ---------------------------------------------------------------------------
def free_rooms_and_places():
    with DBConn.get_session() as session:
        # Підзапит (CTE): для кожного номера рахуємо, скільки людей у ньому живе зараз.
        # outerjoin (LEFT JOIN) потрібен, щоб порожні номери теж потрапили в результат.
        occupancy = (
            select(Room.room_number,
                   RoomType.name.label('type_name'),
                   RoomType.capacity,
                   func.count(Stay.stay_id).label('occupied'))
            .select_from(Room)
            .join(Room.room_type)
            .outerjoin(Stay, and_(Stay.room_id == Room.room_id,
                                  Stay.checkout_date.is_(None)))
            .group_by(Room.room_number, RoomType.name, RoomType.capacity)
            .cte('occupancy')
        )

        # Вільний номер - той, де нікого немає; вільні місця - місткість мінус зайняті.
        summary = select(
            func.count().filter(occupancy.c.occupied == 0).label('free_rooms'),
            func.coalesce(func.sum(occupancy.c.capacity - occupancy.c.occupied), 0)
                .label('free_places'),
        )
        free_rooms, free_places = session.execute(summary).one()

        detail = select(occupancy).order_by(occupancy.c.room_number)
        rows = [(r.room_number, r.type_name, r.capacity, r.occupied,
                 r.capacity - r.occupied)
                for r in session.execute(detail)]

    print()
    print('Запит 4. Вільні номери та вільні місця:')
    print(f'  Вільні номери: {"є" if free_rooms else "немає"}, кількість - {free_rooms}')
    print(f'  Вільні місця:  {"є" if free_places else "немає"}, кількість - {free_places}')
    _print_table('  Розбивка за номерами:',
                 ['Номер', 'Тип', 'Місткість', 'Зайнято', 'Вільно місць'], rows)


def run_all():
    """Виконує всі чотири запити з прикладами параметрів."""
    clients_in_room(101)
    clients_from_city('Харків')
    who_cleaned('ЕК456789', 3)
    free_rooms_and_places()
