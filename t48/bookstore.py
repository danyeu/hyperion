import sqlite3
import sys


# main function
def main():
    # initial state is to use default table
    new_table = True
    try:
        # creating the python_programming table
        cursor.execute("CREATE TABLE books(id INTEGER PRIMARY KEY, Title TEXT, Author TEXT, Qty INTEGER)")
        db.commit()
    except Exception:
        # if table already exists, ask user to use it or to use default table
        print("'books' table already exists",
              "1. Use existing table",
              "2. Use default table",
              sep="\n")
        while True:
            new_table = input("\tEnter 1 or 2: ").strip()
            if new_table not in ["1", "2"]:
                continue
            if new_table == "1":
                new_table = False
            print()
            break
    finally:
        # use default table unless table already exists user entered "1"
        if new_table:
            # default data
            new_data = [(3001, "A Tale of Two Cities", "Charles Dickens", 30),
                        (3002, "Harry Potter and the Philosopher's Stone", "J.K. Rowling", 40),
                        (3003, "The Lion, the Witch and the Wardrobe", "C.S. Lewis", 25),
                        (3004, "The Lord of the Rings", "J.R.R Tolkien", 37),
                        (3005, "Alice in Wonderland", "Lewis Carroll", 12)]
            # delete all rows from 'books' table as it may already have data
            cursor.execute("DELETE FROM books")
            # populate with default data
            cursor.executemany("INSERT INTO books VALUES(?,?,?,?)", new_data)
            db.commit()

    # looping main menu
    while True:
        menu = main_menu()
        if menu == 0:
            print("Exited")
            return
        elif menu == 1:
            add_book()
        elif menu == 2:
            update_book()
        elif menu == 3:
            delete_book()
        elif menu == 4:
            search_books()


# checks if id already exists in database
def id_exists(id: int):
    # select all ids, and loop through them to see if the id already exists
    cursor.execute("SELECT id FROM books")
    for row in cursor:
        if id == row[0]:
            return True
    return False


# main menu
def main_menu():
    # print main menu options
    print(
        "1. Enter book",
        "2. Update book",
        "3. Delete book",
        "4. Search books",
        "0. Exit",
        sep="\n"
    )

    # loop asking for user choice until user enters 0-4
    while True:
        choice = input("\tEnter 0-4: ")
        if choice in ["0", "1", "2", "3", "4"]:
            print()
            return int(choice)


# add a new book to the database
def add_book():
    # ask user for new id, and check if an unused int >0 was entered
    cursor.execute("SELECT id FROM books")
    while True:
        # integer check
        try:
            user_id = int(input("Enter id: ").strip())
        except ValueError:
            print("\tid must be a positive integer")
            continue
        # positive check
        if user_id <= 0:
            print("\tid must be a positive integer")
            continue
        # unused check
        if id_exists(user_id):
            print("\tid already exists")
            continue
        break

    # ask user for new Title, and check if one was entered
    while True:
        user_title = input("Enter Title: ").strip()
        if not user_title:
            print("\tTitle must not be empty")
            continue
        break

    # ask user for new Author, and check if one was entered
    while True:
        user_author = input("Enter Author: ").strip()
        if not user_author:
            print("\tAuthor must not be empty")
            continue
        break

    # ask user for new Qty, and check if an int >=0 was entered
    while True:
        # non-negative integer check
        user_qty = input("Enter Qty: ").strip()
        if not user_qty.isdigit():
            print("\tInvalid Qty")
            continue
        user_qty = int(user_qty)
        break

    # add the new book to the database
    cursor.execute("INSERT INTO books VALUES(?,?,?,?)", (user_id, user_title, user_author, user_qty))
    db.commit()
    print("Added to database\n")


# update an existing book in the database
def update_book():
    # if no books in the database, inform the user and return to main menu
    if count_books() == 0:
        print("No books in database\n")
        return

    # ask for a book id to update
    try:
        # id is valid only if it already exists
        user_id = int(input("Enter book id to update: ").strip())
        if not id_exists(user_id):
            raise ValueError
    except ValueError:
        # if id doesn't exist, inform the user and return to main menu
        print("\tid not found\n")
        return

    # print menu options for what detail to update
    print(
        "Select value to update:",
        "1. id",
        "2. Title",
        "3. Author",
        "4. Qty",
        sep="\n"
    )

    # loop asking for user choice until user enters 1-4
    while True:
        menu = input("\tEnter 1-4: ").strip()
        if menu in ["1", "2", "3", "4"]:
            menu = int(menu)
            break

    # mapping user choice to database column name
    cols = [None, "id", "Title", "Author", "Qty"]

    # generate sql query text based on mapping above
    sql_text = f"SELECT {cols[menu]} FROM books WHERE id = ?"

    # print the old cell value
    cursor.execute(sql_text, (user_id,))
    old_value = cursor.fetchone()[0]
    print(f"Current {cols[menu]}: {old_value}")

    # loop asking for a new valid value
    while True:
        new_value = input("Enter new value: ").strip()
        # all values must not be empty
        if not new_value:
            print(f"\t{cols[menu]} cannot be empty")
            continue
        # id and Qty, must be integers
        if menu == 1 or menu == 4:
            try:
                new_value = int(new_value)
            except ValueError:
                print(f"\t{cols[menu]} must be an integer")
                continue
        # id must be positive
        if menu == 1 and new_value <= 0:
            print(f"\t{cols[menu]} must be a positive integer")
            continue
        # Qty must be non-negative
        if menu == 4 and new_value < 0:
            print(f"\t{cols[menu]} must be a non-negative integer")
            continue
        # id must not already exist
        if menu == 1 and id_exists(new_value):
            print("\tid already exists")
            continue
        break

    # update the database with the new value for that book
    sql_text = f"UPDATE books SET {cols[menu]} = ? WHERE id = ?"
    cursor.execute(sql_text, (new_value, user_id))
    db.commit()
    print("Database updated\n")


# delete an existing book from the database
def delete_book():
    # if no books in the database, inform the user and return to main menu
    if count_books() == 0:
        print("No books in database\n")
        return

    # ask for a book id to delete
    try:
        # id is valid only if it already exists
        user_id = int(input("Enter book id to delete: ").strip())
        if not id_exists(user_id):
            raise ValueError
    except ValueError:
        # if id doesn't exist, inform the user and return to main menu
        print("\tid not found\n")
        return

    # delete the book from the database
    cursor.execute("DELETE FROM books WHERE id = ?", (user_id,))
    db.commit()
    print("Database updated\n")


# search all books, search by id, or search by keyword
def search_books():
    # if no books in the database, inform the user and return to main menu
    if count_books() == 0:
        print("No books in database\n")
        return

    # print menu choices for how to search
    print(
        "1. Search all",
        "2. Search id",
        "3. Search title/author by keyword",
        sep="\n"
    )

    # loop asking for user choice until user enters 1-3
    while True:
        menu = input("\tEnter 1-3: ").strip()
        if menu in ["1", "2", "3"]:
            print()
            break

    # search all
    if menu == "1":
        # select all books in database and print their details
        cursor.execute("SELECT * FROM books")
        for book in cursor:
            print(format_book(book))
        print()
    # search by id
    elif menu == "2":
        # ask for id (return to main menu if non-integer entered)
        try:
            search_id = int(input("Enter id: ").strip())
        except ValueError:
            print("No matches found\n")
            return

        # if id not found in database, return to main menu
        cursor.execute("SELECT COUNT(id) FROM books WHERE id = ?", (search_id,))
        if cursor.fetchone()[0] == 0:
            print("No matches found\n")
            return

        # else if id found in database, print its details
        cursor.execute("SELECT * FROM books WHERE id = ?", (search_id,))
        for book in cursor:
            print(format_book(book))
        print()
    # search by keyword
    else:
        # ask for keyword
        keyword = input("Enter keyword: ").strip()
        # use SQL 'LIKE' to select ids which contain that keyword in the Title or Author columns
        keyword = "%" + keyword + "%"
        cursor.execute("SELECT COUNT(id) FROM books WHERE (Title LIKE ?) OR (Author LIKE ?)", (keyword, keyword))
        # print if no matches found, and return to main menu
        if cursor.fetchone()[0] == 0:
            print("No matches found\n")
            return
        # else if matching books found, print their details
        cursor.execute("SELECT * FROM books WHERE (Title LIKE ?) OR (Author LIKE ?)", (keyword, keyword))
        for book in cursor:
            print(format_book(book))
        print()


# returns user-friendly string of data in one row in the database
def format_book(book: tuple):
    formatted_book = f"id: {book[0]}\n" + f"\tTitle: {book[1]}\n" + f"\tAuthor: {book[2]}\n" + f"\tQty: {book[3]}"
    return formatted_book


# return the number of unique books in the database
def count_books():
    cursor.execute("SELECT COUNT(id) FROM books")
    return cursor.fetchone()[0]


# calling main
if __name__ == '__main__':
    try:
        # initialising the database and its cursor
        db = sqlite3.connect('ebookstore')
        cursor = db.cursor()
    except Exception:
        # if initialisation fails for any reason, exit with an error message
        sys.exit("could not open/create database")
    # call main
    main()
    # disconnect from database when user exits main menu
    db.close()
