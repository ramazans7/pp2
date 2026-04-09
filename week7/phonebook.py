import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="12345678"
)

cur = conn.cursor()
#1
cur.execute("""
CREATE TABLE IF NOT EXISTS phonebook (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    phonenumber VARCHAR(20)
)
""")

conn.commit()
print("Table created")

#2
def add_contact():
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    cur.execute("""
INSERT INTO PhoneBook (name,phonenumber)
VALUES(%s,%s)    
""",(name,phone))
    conn.commit()
    print("Data added")


#3
def show_contacts():
    cur.execute("SELECT * FROM phonebook")
    rows = cur.fetchall()
    for i in rows:
        print(f"ID: {i[0]}, Name: {i[1]}, Phone: {i[2]}")


#4
def update_contact():
    contact_id = input("Enter id: ")
    new_name = input("Enter new name: ")
    cur.execute("UPDATE phonebook SET name = %s WHERE id = %s",(new_name,contact_id))
    conn.commit()
    print("data updated")

#5
def delete_contact():
    contact_id = input("Enter id: ")
    cur.execute("DELETE FROM phonebook WHERE ID = %s",(contact_id,))
    conn.commit()
    print("data deleted")

#6
while True:
    print("1 - Add")
    print("2 - Show")
    print("3 - Update")
    print("4 - Delete")
    print("5 - Exit")

    choice = input("Choose: ")
    if choice == '1':
        add_contact()
    elif choice == '2':
        show_contacts()
    elif choice == '3':
        update_contact()
    elif choice == '4':
        delete_contact()
    elif choice == '5':
        break
    else:
        print("Invalid choice")