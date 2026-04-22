from connect import connect


def search_contacts():
    pattern = input("Enter search pattern: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_contacts(%s)", (pattern,))
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def upsert_contact():
    name = input("Name: ")
    surname = input("Surname: ")
    phone = input("Phone: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL upsert_contact(%s,%s,%s)", (name, surname, phone))

    conn.commit()
    cur.close()
    conn.close()


def bulk_insert():
    names = ["Ali", "John"]
    surnames = ["Khan", "Smith"]
    phones = ["87001112233", "87002223344"]

    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL bulk_insert_contacts(%s,%s,%s)",
                (names, surnames, phones))

    conn.commit()
    cur.close()
    conn.close()


def pagination():
    limit = int(input("Limit: "))
    offset = int(input("Offset: "))

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM get_contacts_paginated(%s,%s)",
        (limit, offset)
    )

    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def delete_contact():
    value = input("Enter name or phone: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL delete_contact(%s)", (value,))

    conn.commit()
    cur.close()
    conn.close()


def menu():
    while True:
        print("\nPhoneBook")
        print("1 Search")
        print("2 Insert/Update")
        print("3 Bulk Insert")
        print("4 Pagination")
        print("5 Delete")
        print("0 Exit")

        choice = input("Choose: ")

        if choice == "1":
            search_contacts()

        elif choice == "2":
            upsert_contact()

        elif choice == "3":
            bulk_insert()

        elif choice == "4":
            pagination()

        elif choice == "5":
            delete_contact()

        elif choice == "0":
            break


if __name__ == "__main__":
    menu()