import json
from connect import get_connection, initialize_db


# ---------- SEARCH EMAIL ----------
def search_email(q):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT name,email FROM contacts WHERE email ILIKE %s", ('%'+q+'%',))
    for i in cur.fetchall():
        print(i)

    conn.close()


# ---------- FILTER GROUP ----------
def filter_group(g):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.name, g.name
        FROM contacts c
        JOIN groups g ON g.id=c.group_id
        WHERE g.name=%s
    """, (g,))

    for i in cur.fetchall():
        print(i)

    conn.close()


# ---------- SORT ----------
def sort_contacts(opt):
    conn = get_connection()
    cur = conn.cursor()

    if opt == "name":
        cur.execute("SELECT name FROM contacts ORDER BY name")
    elif opt == "birthday":
        cur.execute("SELECT name,birthday FROM contacts ORDER BY birthday")
    elif opt == "date":
        cur.execute("SELECT name,created_at FROM contacts ORDER BY created_at")

    for i in cur.fetchall():
        print(i)

    conn.close()


# ---------- PAGINATION ----------
def pagination():
    conn = get_connection()
    cur = conn.cursor()

    limit = 5
    page = 0

    while True:
        cur.execute("SELECT * FROM contacts LIMIT %s OFFSET %s", (limit, page*limit))
        rows = cur.fetchall()

        for r in rows:
            print(r)

        cmd = input("next / prev / quit: ")

        if cmd == "next":
            page += 1
        elif cmd == "prev" and page > 0:
            page -= 1
        elif cmd == "quit":
            break

    conn.close()


# ---------- EXPORT JSON ----------
def export_json():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.name,c.email,c.birthday,g.name,p.phone,p.type
        FROM contacts c
        LEFT JOIN groups g ON g.id=c.group_id
        LEFT JOIN phones p ON p.contact_id=c.id
    """)

    data = []
    for r in cur.fetchall():
        data.append({
            "name": r[0],
            "email": r[1],
            "birthday": str(r[2]),
            "group": r[3],
            "phone": r[4],
            "type": r[5]
        })

    with open("contacts.json", "w") as f:
        json.dump(data, f, indent=4)

    conn.close()
    print("Export OK")


# ---------- IMPORT JSON ----------
def import_json():
    conn = get_connection()
    cur = conn.cursor()

    with open("contacts.json") as f:
        data = json.load(f)

    for c in data:

        cur.execute("SELECT id FROM contacts WHERE name=%s", (c["name"],))
        exists = cur.fetchone()

        if exists:
            ans = input(f"{c['name']} exists (skip/overwrite): ")
            if ans == "skip":
                continue

        cur.execute("""
            INSERT INTO contacts(name,email,birthday)
            VALUES(%s,%s,%s)
            RETURNING id
        """, (c["name"], c["email"], c["birthday"]))

        cid = cur.fetchone()[0]

        cur.execute("""
            INSERT INTO phones(contact_id,phone,type)
            VALUES(%s,%s,%s)
        """, (cid, c["phone"], c["type"]))

    conn.commit()
    conn.close()
    print("Import OK")


# ---------- MAIN ----------
def main():
    print("Initializing DB...")
    initialize_db()

    while True:
        print("""
1 Search email
2 Filter group
3 Sort
4 Pagination
5 Export JSON
6 Import JSON
0 Exit
""")

        c = input("> ")

        if c == "1":
            search_email(input("email: "))
        elif c == "2":
            filter_group(input("group: "))
        elif c == "3":
            sort_contacts(input("name/birthday/date: "))
        elif c == "4":
            pagination()
        elif c == "5":
            export_json()
        elif c == "6":
            import_json()
        elif c == "0":
            break


if __name__ == "__main__":
    main()