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


def contact_add_txt_csv(path_db: str, db_li: list):
    """In progress."""
    os.system('cls')
    with sq.connect(path_db) as con:
        cursor = con.cursor()

    for item in db_li:
        surname = item[1].split(':')[1]
        name = item[2].split(':')[1]
        phone = item[3].split(':')[1]
        phone_type = item[4].split(':')[1]

        query = """ SELECT id, type_of_number FROM types_of_number WHERE type_of_number = ? """
        if cursor.execute(query, (phone_type,)).fetchone() is None:
            query = """ INSERT INTO types_of_number (type_of_number) VALUES (?) """
            cursor.execute(query, (phone_type,))
            con.commit()

        query = """ SELECT id, type_of_number FROM types_of_number WHERE type_of_number = ? """
        phone_type_id = cursor.execute(query, (phone_type,)).fetchone()[0]

        query = """ SELECT phones.id id, phones.phone_number phn, types_of_number.type_of_number typ,
                                    types_of_number.id id_typ
                                    FROM phones, types_of_number WHERE phones.type_id = types_of_number.id 
                                    AND phn = ? """
        if cursor.execute(query, (phone,)).fetchone() is None:
            query = """ INSERT INTO phones (phone_number, type_id) VALUES (?, ?) """
            phone_id = cursor.execute(query, (phone, phone_type_id)).lastrowid
            con.commit()

        query = """ SELECT phones.id id, phones.phone_number phn, types_of_number.type_of_number typ,
                                            types_of_number.id id_typ
                                            FROM phones, types_of_number WHERE phones.type_id = types_of_number.id 
                                            AND phn = ? """
        phone_id = cursor.execute(query, (phone,)).fetchone()[0]

        query = """ SELECT directory.id, users.surname, users.name, phones.phone_number, types_of_number.type_of_number 
                            FROM directory, users, phones, types_of_number
                            WHERE directory.user_id = users.id AND directory.phone_id = phones.id AND 
                            phones.type_id = types_of_number.id AND users.surname = ? AND users.name = ? AND
                            phones.phone_number = ? """
        if cursor.execute(query, (surname, name, phone)).fetchone() is None:
            query = """ INSERT INTO users (surname, name) VALUES (?, ?) """
            user_id = cursor.execute(query, (surname, name)).lastrowid
            con.commit()
            query = """ INSERT INTO directory (phone_id, user_id) VALUES (?, ?) """
            cursor.execute(query, (phone_id, user_id))
            con.commit()
