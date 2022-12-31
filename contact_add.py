import os
import sqlite3 as sq
from pause import pause


def contact_add_manual():
    os.system('cls')
    con = sq.connect('database/phone_directory.db')
    cursor = con.cursor()
    print()
    print('Добавление контакта: ')
    print()
    surname = input('Введите фамилию: ')
    name = input('Введите имя: ')
    phone = input('Введите номер телефона: ')
    phone_type = cursor.execute('''SELECT id, type_of_number FROM types_of_number ''').fetchall()
    print('Выберите тип контакта:')
    for i in range(len(phone_type)):
        print(f'{phone_type[i][0]}. {phone_type[i][1]}')
    contact_type = int(input())
    check_contact = '''SELECT id, surname, name FROM users WHERE surname = ? AND name = ?'''
    check_user_data = cursor.execute(check_contact, (surname, name)).fetchone()
    if check_user_data:
        print('''Указанный контакт обнаружен в справочнике. 
        Добавить новый номер телефона к этому контакту? 
        1. Да
        2. Отмена''')
        choice = int(input())
        if choice == 2:
            print('Добавление контакта отменено!')
            return
        elif choice == 1:
            phone_add_query = '''INSERT INTO phones (phone_number, type_id) VALUES (?, ?);'''
            cursor.execute(phone_add_query, (phone, contact_type))
            con.commit()
            phone_id_query = '''SELECT id FROM phones WHERE phone_number = ?'''
            phone_id_data = cursor.execute(phone_id_query, (phone,)).fetchone()
            add_contact = '''INSERT INTO directory (phone_id, user_id) VALUES (?, ?)'''
            cursor.execute(add_contact, (phone_id_data[0], check_user_data[0]))
            con.commit()
    else:
        user_add_query = '''INSERT INTO users (surname, name) VALUES (?, ?);'''
        data = (surname, name)
        cursor.execute(user_add_query, data)
        con.commit()
        phone_add_query = '''INSERT INTO phones (phone_number, type_id) VALUES (?, ?);'''
        cursor.execute(phone_add_query, (phone, contact_type))
        con.commit()
        user_id_query = '''SELECT id FROM users WHERE surname = ? AND name = ?'''
        user_id_data = cursor.execute(user_id_query, data).fetchone()
        phone_id_query = '''SELECT id FROM phones WHERE phone_number = ?'''
        phone_id_data = cursor.execute(phone_id_query, (phone,)).fetchone()
        add_contact = '''INSERT INTO directory (phone_id, user_id) VALUES (?, ?)'''
        cursor.execute(add_contact, (phone_id_data[0], user_id_data[0]))
        con.commit()
        print('Контакт успешно добавлен!')
    con.close()
    pause()


def get_id(id_li: list, check_id: int) -> int:
    """Get a new id."""
    if check_id not in id_li: return check_id
    new_id = 1
    while id in id_li:
        new_id += 1
    return new_id


def get_id_type_phone(type_phone_li: list, check_type: str) -> int:
    ids = [item[0] for item in type_phone_li]
    for item in type_phone_li:
        if item[1] == check_type:
            return item[0]
    return -1


def contact_add_txt(path_db: str, db_li: list):
    """In progress."""
    os.system('cls')
    """Create dict for next add to DB."""
    con = sq.connect('database/phone_directory_draft.db')
    cursor = con.cursor()
    directory_ids = cursor.execute('''SELECT id FROM directory''').fetchall()
    directory_ids = [item[0] for item in directory_ids]
    users_ids = cursor.execute('''SELECT id FROM users''').fetchall()
    users_ids = [item[0] for item in users_ids]
    phones_ids = cursor.execute('''SELECT id FROM phones''').fetchall()
    phones_ids = [item[0] for item in phones_ids]
    phones_types = cursor.execute('''SELECT id, type_of_number FROM types_of_number''').fetchall()
    phones_types_ids = [item[0] for item in phones_types]

    for items in db_li:
        rec_id = get_id(directory_ids, int(items[0].split(':')[1]))
        new_user_id = get_id(users_ids, 1)
        surname = items[1].split(':')[1]
        name = items[2].split(':')[1]
        new_phone_id = get_id(phones_ids, 1)
        phone = items[3].split(':')[1]
        type_phone = items[4].split(':')[1]
        type_phone_id = get_id_type_phone(phones_types, type_phone)
        if type_phone_id == -1:
            type_phone_id = get_id(phones_types_ids, 1)
            type_phone_add = '''INSERT INTO types_of_number (id, type_of_number) VALUES (?, ?);'''
            cursor.execute(type_phone_add, (type_phone_id, type_phone))
            con.commit()

        add_contact = '''INSERT INTO directory (id, phone_id, user_id) VALUES (?, ?, ?)'''
        cursor.execute(add_contact, (rec_id, new_phone_id, new_user_id))
        con.commit()

        user_add = '''INSERT INTO users (id, surname, name) VALUES (?, ?, ?);'''
        data = (new_user_id, surname, name)
        cursor.execute(user_add, data)
        con.commit()

        phone_add = '''INSERT INTO phones (id, phone_number, type_id) VALUES (?, ?, ?);'''
        cursor.execute(phone_add, (new_phone_id, phone, type_phone_id))
        con.commit()
    con.close()
