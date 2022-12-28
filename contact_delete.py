import os
import sqlite3
from pause import pause


def contact_delete():
    os.system('cls')
    con = sqlite3.connect('database/phone_directory.db')
    cursor = con.cursor()
    print()
    print('''Удаление контакта
    ''')
    print()
    surname_for_delete = input('Введите фамилию: ').capitalize()
    search_query = '''SELECT users.surname, users.name,
                                        phones.phone_number,
                                        types_of_number.type_of_number,
                                        users.id, phones.id
                                        FROM directory
                                        JOIN users ON users.id = directory.user_id 
                                        JOIN phones ON phones.id = directory.phone_id
                                        JOIN types_of_number ON types_of_number.id = phones.type_id
                                        WHERE users.surname = ?
                                        '''
    data = cursor.execute(search_query, (surname_for_delete,)).fetchall()
    if data:
        for contact_number, element in enumerate(data):
            print(contact_number + 1, element[0], element[1], element[2], element[3])
        print()
        print('Выберите контакт для удаления (0 - отмена операции, ALL - удалить всё): ')
        contact_number = input()
        if contact_number == '0':
            return
        elif contact_number == 'ALL':
            delete_phone = '''DELETE FROM phones WHERE phone_number = ?'''
            for item in data:
                cursor.execute(delete_phone, (item[2],))
            con.commit()
            delete_user = '''DELETE FROM users WHERE surname = ?'''
            for item in data:
                cursor.execute(delete_user, (item[0],))
            con.commit()
            delete_directory = '''DELETE FROM directory WHERE user_id = ?'''
            for item in data:
                cursor.execute(delete_directory, (item[4],))
            con.commit()
            print('Данные удалены!')
        else:
            delete_phone = '''DELETE FROM phones WHERE phone_number = ?'''
            cursor.execute(delete_phone, (data[int(contact_number) - 1][2],))
            con.commit()
            delete_directory = '''DELETE FROM directory WHERE phone_id = ?'''
            cursor.execute(delete_directory, (data[int(contact_number) - 1][5],))
            con.commit()
            print('Данные удалены!')
    else:
        print('Контакт не найден')
    print()
    pause()
