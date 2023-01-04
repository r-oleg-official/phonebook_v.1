"""
Задание: возможность подгрузить файл с контактами.
Формат txt через пустую строку:
Фамилия-1
Имя-1
Телефон-1
Описание-1

Фамилия-2
Имя-2
Телефон-2
Описание-2
...
Формат txt через разделитель, напр.: "," ";": (можно сделать выбор)
Фамилия-1,Имя-1,Телефон-1,Описание-1
Фамилия-2,Имя-2,Телефон-2,Описание-2

Мой вариант формата txt:
begin
id:1
ln:family-1
fn:name-1
tel:+79101111111
type:home
end

Еще раз основная задача на текущий момент - из файла txt и csv получить список всех
данных и просто вывести на экран для начала.

Структура списка: ["ID", "Фамилия", "Имя", "телефон", "вид телефона"].

Потом надо будет это в кортежах передать в бД.
...Чисто для коммента...
"""

from contact_add import contact_add_txt_csv
import csv


def read_file_txt(path: str) -> list:
    with open(path, 'r') as file:
        data = file.read()
        li_res = data.split("\n")
        li_res = [item for item in li_res if item != 'begin' and item != 'end' and item != '']
    return li_res


def read_file_csv(path: str) -> list:
    with open(path, "r", encoding="UTF-8") as file:
        data = [row for row in csv.reader(file)]

    headers = data[0]
    data = data[1:]

    for item in data:
        for i in range(len(item)):
            item[i] = f'{headers[i]}:{item[i]}'
    return data


def write_file(path: str, line: str):
    with open(path, 'w') as file:
        file.writelines(line)


def append_file(path: str, line: str):
    with open(path, 'a') as file:
        file.writelines(line)


def determine_file_extension(file: str) -> str:
    return file.split('.')[1]


def parse_db_txt(li: list):
    start_pos: int = 1
    li_res = []
    for i in range(0, len(li) - 4, 5):
        li_res.append(li[i: i + 5])
    return li_res


def import_from_file():
    """In progress."""
    print('Импорт контактов')
    print()
    type_file = input("Формат файла импорта (1 - txt, 2 - csv): ")
    match type_file:
        case '1':
            path_to_db = "database/phone_directory.db"
            path_import = "database/phone_db.txt"
            list_import = read_file_txt(path_import)
            contact_add_txt_csv(path_to_db, parse_db_txt(list_import))
        case '2':
            path_to_db = "database/phone_directory.db"
            path_import = "database/phone_db.csv"
            list_import = read_file_csv(path_import)
            contact_add_txt_csv(path_to_db, parse_db_txt(list_import))
        case _:
            return


def import_from_file_v2():
    """Import from user's input path to file for import."""
    print('Импорт контактов')
    print()
    file_extension = determine_file_extension(input("Путь/имя_файла: "))
    match file_extension:
        case 'txt':
            db = 'database/phone_db.txt'
        case 'csv':
            db = 'database/phone_db.csv'
        case _:
            return
