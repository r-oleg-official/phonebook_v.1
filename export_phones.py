import os
import sqlite3
from pause import pause
import csv


def write_file(path: str, line: str):
    """In progress."""
    with open(path, 'w') as file:
        file.writelines(line)


def append_file(path: str, line: str):
    """In progress."""
    with open(path, 'a') as file:
        file.writelines(line)


def export_phones():
    os.system('cls')
    print('Экспорт телефонной книги')
    print()
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
    print(result_dictionary)
    print()
    print('''Выберите формат экспорта:
    1. Линия
    2. Столбик
    ''')
    choice = input()
    with open('export.csv', mode="w", encoding='utf-8') as export_file:
        if choice == '1':
            file_writer = csv.writer(export_file, delimiter=';', lineterminator="\r")
            file_writer.writerow(["Фамилия Имя", "Номер телефона", "Тип контакта"])
            for key, data in result_dictionary.items():
                row = [key]
                for item in data:
                    row.append(item)
                file_writer.writerow(row)
        elif choice == '2':
            file_writer = csv.writer(export_file, delimiter=';', lineterminator="\r")
            for key in result_dictionary.keys():
                row = ['Фамилия Имя']
                row.append(key)
                file_writer.writerow(row)
                row = ['Номер телефона']
                for item in result_dictionary[key]:
                    row.append(item)
                file_writer.writerow(row)
                row.clear()
        else:
            return
        print('Экспорт успешно завершен.')
        print('Контакты сохранены в файл export_line.csv')
        print('Кодировка файла - UTF-8')
        print()
    pause()
