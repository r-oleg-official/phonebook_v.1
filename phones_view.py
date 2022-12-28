import os
import sqlite3
from pause import pause


def phones_view():
    os.system('cls')
    con = sqlite3.connect('database/phone_directory.db')
    cursor = con.cursor()

    data = cursor.execute('''SELECT users.surname, users.name,
                                    phones.phone_number,
                                    types_of_number.type_of_number
                            FROM directory
                            JOIN users ON users.id = directory.user_id 
                            JOIN phones ON phones.id = directory.phone_id
                            JOIN types_of_number ON types_of_number.id = phones.type_id
                            ORDER BY users.surname
                            ''').fetchall()
    result_dictionary = {}
    for element in data:
        if f'{element[0]} {element[1]}' not in result_dictionary:
            result_dictionary[f'{element[0]} {element[1]}'] = (element[2], element[3])
        else:
            result_dictionary[f'{element[0]} {element[1]}'] += (element[2], element[3])
    for key in result_dictionary.keys():
        print(f'Фамилия Имя: {key}')
        for i in range(0, len(result_dictionary[key]), 2):
            print(f'Номер телефона: {result_dictionary[key][i]}')
            print(f'Тип контакта: {result_dictionary[key][i + 1]}')
        print()

    con.close()
    pause()
