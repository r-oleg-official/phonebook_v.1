import os
import sqlite3
from pause import pause


def contact_add():
    os.system('cls')
    con = sqlite3.connect('database/phone_directory.db')
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
    