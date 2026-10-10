
import datetime
 
from sqlalchemy import select, func
 
from api.engine import DBConn
from models.room_type import RoomType
from models.room import Room
from models.client import Client
from models.stay import Stay
from models.employee import Employee
from models.cleaning_schedule import CleaningSchedule
 
 
def fill_db():
    with DBConn.get_session() as session:
 
        # Паспорти та номери кімнат унікальні, тому повторний запуск закінчився б помилкою.
        # Щоб цього не було, спершу перевіряємо, чи база вже заповнена.
        if session.scalar(select(func.count()).select_from(RoomType)) > 0:
            print('База вже містить дані. Щоб заповнити заново: '
                  'drop-tables, create-tables, fill-db.')
            return
 
        # --- Типи номерів (3 рядки) ---
        single = RoomType(name='одномісний', capacity=1, price_per_day=800)
        double = RoomType(name='двомісний', capacity=2, price_per_day=1300)
        triple = RoomType(name='тримісний', capacity=3, price_per_day=1700)
 
        # --- Номери (8 рядків) ---
        # Тип номера вказуємо ОБ'ЄКТОМ (room_type=single), а не числовим id:
        # SQLAlchemy сама визначить значення зовнішнього ключа під час збереження.
        room_list = [
            Room(room_number=101, floor=1, phone='+380441234501', room_type=single),
            Room(room_number=102, floor=1, phone='+380441234502', room_type=single),
            Room(room_number=103, floor=1, phone='+380441234503', room_type=double),
            Room(room_number=201, floor=2, phone='+380441234504', room_type=double),
            Room(room_number=202, floor=2, phone='+380441234505', room_type=double),
            Room(room_number=203, floor=2, phone='+380441234506', room_type=triple),
            Room(room_number=301, floor=3, phone='+380441234507', room_type=triple),
            Room(room_number=302, floor=3, phone='+380441234508', room_type=single),
        ]
        rooms = {r.room_number: r for r in room_list}   # щоб шукати номер за його номером
 
        # --- Клієнти (7 рядків) ---
        client_list = [
            Client(passport_number='ЕК123456', last_name='Коваленко', first_name='Олена',
                   patronymic='Іванівна', city='Харків'),
            Client(passport_number='ЕК234567', last_name='Шевченко', first_name='Андрій',
                   patronymic='Петрович', city='Львів'),
            Client(passport_number='ЕК345678', last_name='Бондаренко', first_name='Марія',
                   patronymic='Сергіївна', city='Одеса'),
            Client(passport_number='ЕК456789', last_name='Мельник', first_name='Дмитро',
                   patronymic='Олександрович', city='Харків'),
            Client(passport_number='ЕК567890', last_name='Ткаченко', first_name='Наталія',
                   patronymic='Василівна', city='Дніпро'),
            Client(passport_number='ЕК678901', last_name='Кравченко', first_name='Ігор',
                   patronymic='Миколайович', city='Львів'),
            Client(passport_number='ЕК789012', last_name='Поліщук', first_name='Софія',
                   patronymic='Андріївна', city='Київ'),
        ]
        clients = {c.passport_number: c for c in client_list}
 
        # --- Службовці (5 рядків) ---
        honchar = Employee(last_name='Гончар', first_name='Тетяна', patronymic='Олексіївна')
        savchenko = Employee(last_name='Савченко', first_name='Віктор', patronymic='Іванович')
        lysenko = Employee(last_name='Лисенко', first_name='Ольга', patronymic='Дмитрівна')
        romaniuk = Employee(last_name='Романюк', first_name='Сергій', patronymic='Петрович')
        danylenko = Employee(last_name='Даниленко', first_name='Юлія', patronymic='Андріївна')
 
        # --- Проживання (8 рядків: чотири тривають зараз, решта завершені) ---
        # Клієнта й номер теж вказуємо об'єктами. checkout_date=None означає "ще живе".
        d = datetime.date
        stay_list = [
            Stay(client=clients['ЕК123456'], room=rooms[101], checkin_date=d(2026, 8, 1), checkout_date=d(2026, 8, 5)),
            Stay(client=clients['ЕК234567'], room=rooms[102], checkin_date=d(2026, 8, 3), checkout_date=d(2026, 8, 10)),
            Stay(client=clients['ЕК345678'], room=rooms[201], checkin_date=d(2026, 8, 15), checkout_date=None),
            Stay(client=clients['ЕК456789'], room=rooms[101], checkin_date=d(2026, 8, 20), checkout_date=None),
            Stay(client=clients['ЕК567890'], room=rooms[203], checkin_date=d(2026, 8, 10), checkout_date=d(2026, 8, 14)),
            Stay(client=clients['ЕК678901'], room=rooms[301], checkin_date=d(2026, 8, 25), checkout_date=None),
            Stay(client=clients['ЕК789012'], room=rooms[103], checkin_date=d(2026, 9, 1), checkout_date=d(2026, 9, 5)),
            Stay(client=clients['ЕК123456'], room=rooms[202], checkin_date=d(2026, 9, 6), checkout_date=None),
        ]
 
        # --- Графік прибирання (10 рядків: по 2 дні на службовця, поверхи різні) ---
        schedule_list = [
            CleaningSchedule(employee=honchar, weekday=1, floor=1),
            CleaningSchedule(employee=honchar, weekday=4, floor=2),
            CleaningSchedule(employee=savchenko, weekday=1, floor=2),
            CleaningSchedule(employee=savchenko, weekday=3, floor=3),
            CleaningSchedule(employee=lysenko, weekday=2, floor=1),
            CleaningSchedule(employee=lysenko, weekday=5, floor=1),
            CleaningSchedule(employee=romaniuk, weekday=2, floor=3),
            CleaningSchedule(employee=romaniuk, weekday=6, floor=2),
            CleaningSchedule(employee=danylenko, weekday=3, floor=1),
            CleaningSchedule(employee=danylenko, weekday=7, floor=3),
        ]
 
        # Додаємо все в сесію й зберігаємо одним commit. Порядок вставки (спершу батьківські
        # таблиці, потім дочірні) SQLAlchemy визначає сама за зовнішніми ключами.
        session.add_all([single, double, triple])
        session.add_all(room_list)
        session.add_all(client_list)
        session.add_all([honchar, savchenko, lysenko, romaniuk, danylenko])
        session.add_all(stay_list)
        session.add_all(schedule_list)
        session.commit()
 
        print(f'Додано: типів номерів - 3, номерів - {len(room_list)}, '
              f'клієнтів - {len(client_list)}, службовців - 5, '
              f'проживань - {len(stay_list)}, записів графіка - {len(schedule_list)}')