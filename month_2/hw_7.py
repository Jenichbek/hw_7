import sqlite3

connection = sqlite3.connect("library.db")
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        author TEXT,
        year INTEGER,
        available INTEGER
    )
""")
connection.commit()

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

cursor.execute("SELECT * FROM books")
books = cursor.fetchall()

print("Список книг:")
for book in books:
    print(book)

def show_books():
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    if not books:
        print("В библиотеке пока нет книг")
        return
    for b in books:
        status = "в наличии" if b[4] else "нет в наличии"
        print(f"{b[0]}. {b[1]} - {b[2]}, {b[3]} ({status})")


def find_book():
    title = input("Введите название (или часть): ").lower()
    cursor.execute("SELECT * FROM books")
    found = [b for b in cursor.fetchall() if title in b[1].lower()]
    if not found:
        print("Книга не найдена")
        return
    for b in found:
        status = "в наличии" if b[4] else "нет в наличии"
        print(f"{b[0]}. {b[1]} - {b[2]}, {b[3]} ({status})")


def add_book():
    name = input("Название: ")
    author = input("Автор: ")
    try:
        year = int(input("Год издания: "))
    except ValueError:
        print("Год должен быть числом")
        return
    cursor.execute(
        "INSERT INTO books (name, author, year, available) VALUES (?, ?, ?, ?)",
        (name, author, year, 1)
    )
    connection.commit()
    print("Книга добавлена")
connection.commit()

def update_book():
    show_books()
    try:
        book_id = int(input("Введите id книги для изменения: "))
    except ValueError:
        print("id должен быть числом")
        return
    name = input("Новое название: ")
    author = input("Новый автор: ")
    try:
        year = int(input("Новый год: "))
    except ValueError:
        print("Год должен быть числом")
        return
    cursor.execute(
        "UPDATE books SET name = ?, author = ?, year = ? WHERE id = ?",
        (name, author, year, book_id)
    )
    connection.commit()
    print("Данные обновлены" if cursor.rowcount else "Книга с таким id не найдена")


def delete_book():
    show_books()
    try:
        book_id = int(input("Введите id книги для удаления: "))
    except ValueError:
        print("id должен быть числом")
        return
    if input("Точно удалить? (да/нет): ").lower() != "да":
        print("Отменено")
        return
    cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
    connection.commit()
    print("Книга удалена" if cursor.rowcount else "Книга с таким id не найдена")


def main():
    while True:
        print("\nБиблиотека")
        print("1. Показать все книги")
        print("2. Найти книгу по названию")
        print("3. Добавить книгу")
        print("4. Изменить книгу")
        print("5. Удалить книгу")
        print("0. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            show_books()
        elif choice == "2":
            find_book()
        elif choice == "3":
            add_book()
        elif choice == "4":
            update_book()
        elif choice == "5":
            delete_book()
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Неверный выбор, введите число от 0 до 5")

    connection.close()


main()