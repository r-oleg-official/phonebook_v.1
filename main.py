""" Задание в группах: Создать телефонный справочник с возможностью импорта и экспорта данных в нескольких форматах."""

import os
from phones_view import phones_view
from user_interface import user_interface
from exit import exit
from contact_search import contact_search
from contact_add import contact_add
from contact_delete import contact_delete
from import_from_file import import_from_file
from export_phones import export_phones
import global_variables as gv


def main():
    functions = {1: lambda: phones_view(),
                 2: lambda: contact_search(),
                 3: lambda: contact_add(),
                 4: lambda: contact_delete(),
                 5: lambda: import_from_file(),
                 6: lambda: export_phones(),
                 7: lambda: exit()}

    while gv.choose_move != 7:
        os.system('cls')
        user_interface()
        if functions.get(gv.choose_move) is not None:
            functions[gv.choose_move]()


if __name__ == "__main__":
    main()
