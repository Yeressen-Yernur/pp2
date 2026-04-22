import psycopg2
import csv
from connect import connect


def insert_from_console():
    name = input("Enter name: ")
    phone = input("Enter phone: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO contacts (name, phone) VALUES (%s, %s)",
        (name, phone)
    )

    conn.commit()
    cur.close()
    conn.close()

    print("Contact added.")


def insert_from_csv(filename):
    conn = connect()
    cur = conn.cursor()

    with open(filename, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)

        for row in reader:
            name, phone = row
            cur.execute(
                "INSERT INTO contacts (name, phone) VALUES (%s, %s)",
                (name, phone)
            )

    conn.commit()
    cur.close()
    conn.close()

    print("CSV data imported.")


def update_contact():
    name = input("Enter name to update: ")
    new_phone = input("Enter new phone: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "UPDATE contacts SET phone=%s WHERE name=%s",
        (new_phone, name)
    )

    conn.commit()
    cur.close()
    conn.close()

    print("Contact updated.")


def query_contacts():
    filter_name = input("Enter name filter (or press enter): ")

    conn = connect()
    cur = conn.cursor()

    if filter_name:
        cur.execute(
            "SELECT * FROM contacts WHERE name ILIKE %s",
            ('%' + filter_name + '%',)
        )
    else:
        cur.execute("SELECT * FROM contacts")

    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def delete_contact():
    value = input("Enter name or phone to delete: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM contacts WHERE name=%s OR phone=%s",
        (value, value)
    )

    conn.commit()
    cur.close()
    conn.close()

    print("Contact deleted.")


def menu():
    while True:
        print("\nPhoneBook Menu")
        print("1 - Insert contact")
        print("2 - Import from CSV")
        print("3 - Update contact")
        print("4 - Query contacts")
        print("5 - Delete contact")
        print("0 - Exit")

        choice = input("Choose: ")

        if choice == "1":
            insert_from_console()
        elif choice == "2":
            insert_from_csv("contacts.csv")
        elif choice == "3":
            update_contact()
        elif choice == "4":
            query_contacts()
        elif choice == "5":
            delete_contact()
        elif choice == "0":
            break


if __name__ == "__main__":
    menu()