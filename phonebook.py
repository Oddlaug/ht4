# -*- coding: utf-8 -*-
import os
import pickle


def dump_list(func):
    def wrapper(file, data):
        data = data if isinstance(data, list) else []
        return func(file, data)

    return wrapper


def load_list(func):
    def wrapper(file):
        lst = func(file)
        return lst if isinstance(lst, list) else []

    return wrapper


@load_list
def load_book(book_file: str) -> list:
    """Загрузить список из двоичного файла"""
    try:
        with open(book_file, 'rb') as f:
            return pickle.load(f)
    except pickle.PickleError as e:
        print(f'Неподдерживаемый формат файла => {e}')


@dump_list
def save_book(book_file: str, data: object) -> None:
    """Сохранить список в двоичном файле"""
    with open(book_file, 'wb') as f:
        pickle.dump(data, f)


def is_exists(file: str) -> bool:
    """Проверить, существует ли файл"""
    return os.path.exists(file) and os.path.isfile(file)


class Contact:
    def __init__(self, first_name, last_name, phone, favorite=False, **kwargs):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.favorite = favorite
        self.additional = kwargs

    def __eq__(self, other):
        """Сравнить объекты по атрибутам"""
        return self.__dict__ == other.__dict__

    def __str__(self):
        if self.additional:
            s = """\nДополнительная инофрмация:"""
            for kwarg in self.additional:
                s += f'\n\t\t{kwarg}: {self.additional[kwarg]}'
        else:
            s = ''
        return f"""
Имя: {self.first_name}
Фамилия: {self.last_name}
Телефон: {self.phone}
В избранных: {'да' if self.favorite else 'нет'}""" + s


class PhoneBook:
    def __init__(self, adress_book_file):
        if is_exists(adress_book_file):
            self.book_file = adress_book_file
        else:
            raise Exception(f'Файл {adress_book_file} не существует!')

    def show_contacts(self) -> None:
        """Отображение всех контактов телефонной книги"""
        contacts = load_book(self.book_file)
        if contacts:
            for contact in contacts:
                print(contact)
        else:
            print('Телефонная книга пуста')

    def add_contact(self, new_contact: object) -> None:
        """ Добавить новый контакт"""
        if isinstance(new_contact, Contact):
            contacts = load_book(self.book_file)
            for contact in contacts:
                if contact == new_contact:
                    print('Такой контакт уже есть!')
                    return
            contacts.append(new_contact)
            save_book(self.book_file, contacts)
        else:
            raise Exception('Недопустимый формат контакта')

    def remove_contact_by_phone(self, phone: str) -> None:
        """Удалить контакт по номеру телефона"""
        contacts = load_book(self.book_file)
        phone_exists = False
        if contacts:
            for contact in contacts:
                if contact.phone == phone:
                    phone_exists = True
                    contacts.remove(contact)
                    print(f'Контакт {contact.first_name} {contact.last_name} удален!')
            if not phone_exists:
                print(f'Номер "{phone}" не найден!')
            save_book(self.book_file, contacts)
        else:
            print('Телефонная книга не содержит контактов')

    def find_favorites(self) -> None:
        """ Показать телефоны избранных контактов"""
        contacts = load_book(self.book_file)
        favorite_exists = False
        if contacts:
            for contact in contacts:
                if contact.favorite is True:
                    favorite_exists = True
                    print(contact.phone)
            if not favorite_exists:
                print('Избранных контактов не обнаружено!')
        else:
            print('Телефонная книга не содержит контактов!')

    def find_by_fullname(self, f_name: str, l_name: str):
        """ Вывести информацию по полному имени контакта"""
        contacts = load_book(self.book_file)
        contact_exists = False
        if contacts:
            for contact in contacts:
                if contact.first_name == f_name and contact.last_name == l_name:
                    print(contact)
                    contact_exists = True
            if not contact_exists:
                print(f'Контакт "{f_name} {l_name}" не найден!')
        else:
            print('Телефонная книга не содержит контактов')


def factory(f_name):
    return PhoneBook(f_name)


def main():
    book_file = ''
    while True:
        print(
            """
                        Приложение "Телефонная книга"
            1 - создать новую книгу
            2 - загрузить книгу
            3 - показать все контакты
            4 - добавить новый контакт
            5 - удалить контакт по номеру телефона
            6 - показать телефонные номера избранных контактов
            7 - вывести инофрмацию по полному имени контакта
            q - завершение работы програмы\n\n
            """)
        choice = input('Выберите нужный вариант:')

        if choice.lower().strip() == 'q':
            break
        elif choice.strip() == '1':
            book = input("Введите имя файла телефонной книги: ")
            try:
                save_book(book, [])
                print(f'Создана пустая книга (файл {book})')
            except OSError:
                print('Недопустимое имя файла!')

        elif choice.strip() == '2':
            user_file = input("Введите имя файла телефонной книги: ")
            if is_exists(user_file):
                book_file = user_file
            else:
                print(f'Файл "{user_file}" телефонной книги на найден!')

        elif choice.strip() == '3':
            if book_file:
                factory(book_file).show_contacts()
            else:
                print('Не загружена телефонная книга!')

        elif choice.strip() == '4':
            favorite = False
            additional = dict()
            if book_file:
                first_name = input('Имя: ')
                last_name = input('Фамилия: ')
                phone = input("Номер телефона: ")
                favorite_answer = input('Добавить в избранное (y/n):')
                if favorite_answer.lower().strip() == 'y':
                    favorite = True
                addition = input('Добавить дополнительную инофрмацию (y/n):')
                if addition.lower().strip() == 'y':
                    while True:
                        field = input('Название поля: ')
                        data = input('Значение поля: ')
                        additional.update({field: data})
                        question = input('Добавить еще данные (y/n)')
                        if question.lower().strip() == 'n':
                            break
                factory(book_file).add_contact(Contact(first_name, last_name, phone, favorite=favorite, **additional))
            else:
                print('Не загружена телефонная книга!')

        elif choice.strip() == '5':
            if book_file:
                phone = input('Номер телефона: ')
                factory(book_file).remove_contact_by_phone(phone)
            else:
                print('Не загружена телефонная книга!')

        elif choice.strip() == '5':
            if book_file:
                phone = input('Номер телефона: ')
                factory(book_file).remove_contact_by_phone(phone)
            else:
                print('Не загружена телефонная книга!')

        elif choice.strip() == '6':
            if book_file:
                factory(book_file).find_favorites()
            else:
                print('Не загружена телефонная книга!')

        elif choice.strip() == '7':
            if book_file:
                first_name = input('Имя пользователя: ')
                last_name = input('Фамилия пользователя: ')
                factory(book_file).find_by_fullname(first_name, last_name)
            else:
                print('Не загружена телефонная книга!')

        else:
            pass


if __name__ == '__main__':
    main()
