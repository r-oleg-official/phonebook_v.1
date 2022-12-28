import os
import sqlite3
from pause import pause


def contact_search():
    os.system('cls')
    con = sqlite3.connect('database/phone_directory.db')
    cursor = con.cursor()
    print()
    print('''Поиск контакта: 

    1. По фамилии
    2. По имени
    3. По номеру телефона
    4. Отмена

    ''')
    print()
    search_type = int(input('Выберите действие: '))
    if search_type == 1:
        surname = input('Введите фамилию: ').capitalize()
        search_query = '''SELECT users.surname, users.name,
                                    phones.phone_number,
                                    types_of_number.type_of_number
                                    FROM directory
                                    JOIN users ON users.id = directory.user_id 
                                    JOIN phones ON phones.id = directory.phone_id
                                    JOIN types_of_number ON types_of_number.id = phones.type_id
                                    WHERE users.surname = ?
                                    '''
        data = cursor.execute(search_query, (surname,)).fetchall()
        if data:
            for element in data:
                print(element[0], element[1], element[2], element[3])
        else:
            print('Контакт не найден')
    elif search_type == 2:
        name = input('Введите имя: ').capitalize()
        search_query = '''SELECT users.surname, users.name,
                                            phones.phone_number,
                                            types_of_number.type_of_number
                                            FROM directory
                                            JOIN users ON users.id = directory.user_id 
                                            JOIN phones ON phones.id = directory.phone_id
                                            JOIN types_of_number ON types_of_number.id = phones.type_id
                                            WHERE users.name = ?
                                            '''
        data = cursor.execute(search_query, (name,)).fetchall()
        if data:
            for element in data:
                print(element[0], element[1], element[2], element[3])
        else:
            print('Контакт не найден')
    elif search_type == 3:
        phone = input('Введите номер телефона: ')
        search_query = '''SELECT users.surname, users.name,
                                                    phones.phone_number,
                                                    types_of_number.type_of_number
                                                    FROM directory
                                                    JOIN users ON users.id = directory.user_id 
                                                    JOIN phones ON phones.id = directory.phone_id
                                                    JOIN types_of_number ON types_of_number.id = phones.type_id
                                                    WHERE phones.phone_number = ?
                                                    '''
        data = cursor.execute(search_query, (phone,)).fetchall()
        if data:
            for element in data:
                print(element[0], element[1], element[2], element[3])
        else:
            print('Контакт не найден')
    else:
        return
    con.close()
    print()
    pause()
