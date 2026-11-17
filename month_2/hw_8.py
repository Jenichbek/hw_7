from abc import ABC, abstractmethod #здесь мы говорим что в этом файле мы будем использовать абстрактные классы и методы
from datetime import date #здесь мы импортируем модуль date из библиотеки datetime, чтобы работать с датами


class LibraryItem(ABC):
    def __init__(self, name):
        self.__name = name  

    @property #здесь мы используем декоратор @property, чтобы сделать метод name доступным как атрибут
    def name(self):
        return self.__name

    @name.setter #здесь мы используем декоратор @name.setter, чтобы сделать метод name доступным для изменения
    def name(self, new_name):
        if not new_name.strip():
            raise ValueError("Название не может быть пустым")
        print(f"Название изменено с «{self.__name}» на «{new_name}»")
        self.__name = new_name

    @abstractmethod 
    def get_info(self) -> str:
        pass



class Book(LibraryItem):  #наследует от главного класса
    def __init__(self, name, author, year):
        super().__init__(name)
        if not Book.is_valid_year(year):
            raise ValueError(f"Некорректный год: {year}")
        self.author = author
        self.year = year
    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["author"], data["year"])
    @classmethod
    def from_string(cls, text):
        name, author, year = text.split(";")
        return cls(name.strip(), author.strip(), int(year))

    def get_info(self):
        return f"«{self.name}», автор: {self.author}, год: {self.year}"

    def __str__(self):
        return f"Книга: {self.get_info()}"
class JsonExportMixin(Book):
    def to_dict(self):
        return {
            "name": self.name,
            "author": self.author,
            "year": self.year
        }


    @staticmethod
    def is_valid_year(year):
        return isinstance(year, int) and 0 < year <= date.today().year

    def get_info(self):
        return f"«{self.name}», автор: {self.author}, год: {self.year}"

    def __str__(self):
        return f"Книга: {self.get_info()}"

    def __eq__(self, other):
        if not isinstance(other, Book):
            return NotImplemented
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)


class AudioBook(Book):
    def __init__(self, name, author, year, duration):
        super().__init__(name, author, year)
        self.duration = duration

    def get_info(self):
        return f"{super().get_info()}, продолжительность: {self.duration} мин."

    def __str__(self):
        return f"Аудиокнига: {self.get_info()}"

class Mixin(JsonExportMixin, AudioBook, Book, LibraryItem):
    pass

def find_book(library, title): #здесь мы пишем код для поиска книги в библиотке по названию
    checks = 0
    for book in library:
        checks += 1
        if book.name.lower() == title.lower():
            return book, checks
    return None, checks

import sqlite3 #говорим что мы будем использовать Sqlite

connection = sqlite3.connect("library1.db")
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        author TEXT,
        year INTEGER,
        available INTEGER
    )
""") #тут мы создаем таблицу books, если она не существует, с полями id, name, author, year и available
connection.commit() #после этого мы сохраняем изменения в базе данных

books = [
    ("The Great Gatsby", "F. Scott Fitzgerald", "1925", "Yes"),
    ("To Kill a Mockingbird", "Harper Lee", "1960", "Yes"),
    ("1984", "George Orwell", "1948", "No")
]

cursor.executemany(
    "INSERT INTO books (name, author, year, available) VALUES (?,?,?,?)",
    books   
)

connection.commit()
#здесь я использовал быстрый метод добавления записей в таблицу 

def add_book(): #для того что бы добавить книги в так называемую библиотеку
    name = input("Название: ")
    author = input("Автор: ")
    try:
        year = int(input("Год издания: "))
    except ValueError:
        print("Год должен быть числом")
        return
    cursor.execute(
        "INSERT INTO books (name, author, year, available) VALUES (?, ?, ?, ?)",
        (name, author, year, 1),
    )
    connection.commit()
    print("Книга добавлена")


def show_books(): #фуекция для того что бы показать книги в библиотеке
    cursor.execute("SELECT * FROM books")
    rows = cursor.fetchall()
    if not rows:
        print("В библиотеке пока нет книг")
        return
    for b in rows:
        status = "в наличии" if b[4] else "нет в наличии"
        print(f"{b[0]}. {b[1]} - {b[2]}, {b[3]} ({status})")


def update_book():#фуекция для того что бы изменить данные о книге
    show_books() #снчала функция будет показывать весь список книг в бтблиотеке
    try:
        book_id = int(input("id книги для изменения: "))
        name = input("Новое название: ")
        author = input("Новый автор: ")
        year = int(input("Новый год: "))
    except ValueError:
        print("id и год должны быть числами")
        return
    cursor.execute(
        "UPDATE books SET name = ?, author = ?, year = ? WHERE id = ?",
        (name, author, year, book_id),
    )
    connection.commit()
    print("Данные обновлены" if cursor.rowcount else "Книга с таким id не найдена")


def delete_book(): #фуекция для того что бы удалить книгу из библиотеки
    show_books()
    try:
        book_id = int(input("id книги для удаления: "))
    except ValueError:
        print("id должен быть числом")
        return
    cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
    connection.commit()
    print("Книга удалена" if cursor.rowcount else "Книга с таким id не найдена")


while True: #так скажем менб программы
    print("\n1. Добавить книгу")
    print("2. Показать все книги")
    print("3. Изменить книгу")
    print("4. Удалить книгу")
    print("0. Выход")
    choice = input("Выберите действие: ")

    if choice == "1":
        add_book()
    elif choice == "2":
        show_books()
    elif choice == "3":
        update_book()
    elif choice == "4":
        delete_book()
    elif choice == "0":
        break
    else:
        print("Неверный выбор")

connection.close() #и закрываем соединение с базой данных в конце программы