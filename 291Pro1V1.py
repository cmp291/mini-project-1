import sqlite3
import time
import hashlib

connection = None
cursor = None

def connect(path):
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA forteign_keys=ON; ')
    connection.commit()
    return

# Drop tables
def drop_tables():
    global connection, cursor

    drop_requests = '''drop table if exists requests;'''
    drop_enroute = '''drop table if exists enroute;'''
    drop_bookings = '''drop table if exists bookings;'''
    drop_rides = '''drop table if exists rides;'''
    drop_locations = '''drop table if exists locations;'''
    drop_cars = '''drop table if exists cars;'''
    drop_members = '''drop table if exists members;'''
    drop_inbox = '''drop table if exists inbox;'''

    cursor.execute(drop_requests)
    cursor.execute(drop_enroute)
    cursor.execute(drop_bookings)
    cursor.execute(drop_rides)
    cursor.execute(drop_locations)
    cursor.execute(drop_cars)
    cursor.execute(drop_members)
    cursor.execute(drop_inbox)
    connection.commit()
    return

# Define tables
def define_tables():
    global connection, cursor
    members_Table= ''' create table members (
      email		char(15),
      name		char(20),
      phone		char(12),
      pwd		char(6),
      primary key (email)
    );'''
    cars_Table = ''' create table cars (
      cno		int,
      make		char(12),
      model		char(12),
      year		int,
      seats		int,
      owner		char(15),
      primary key (cno),
      foreign key (owner) references members
    );'''
    locations_Table = '''create table locations (
      lcode		char(5),
      city		char(16),
      prov		char(16),
      address	char(16),
      primary key (lcode)
    );'''
    rides_Table = '''create table rides (
      rno		int,
      price		int,
      rdate		date,
      seats		int,
      lugDesc	char(10),
      src		char(5),
      dst		char(5),
      driver	char(15),
      cno		int,
      primary key (rno),
      foreign key (src) references locations,
      foreign key (dst) references locations,
      foreign key (driver) references members,
      foreign key (cno) references cars
    );'''
    bookings_Table = '''create table bookings (
      bno		int,
      email		char(15),
      rno		int,
      cost		int,
      seats		int,
      pickup	char(5),
      dropoff	char(5),
      primary key (bno),
      foreign key (email) references members,
      foreign key (rno) references rides,
      foreign key (pickup) references locations,
      foreign key (dropoff) references locations
    );'''
    enroute_Table = '''create table enroute (
      rno		int,
      lcode		char(5),
      primary key (rno,lcode),
      foreign key (rno) references rides,
      foreign key (lcode) references locations
    );'''
    requests_Table = '''create table requests (
      rid		int,
      email		char(15),
      rdate		date,
      pickup	char(5),
      dropoff	char(5),
      amount	int,
      primary key (rid),
      foreign key (email) references members,
      foreign key (pickup) references locations,
      foreign key (dropoff) references locations
    );'''
    inbox_Table = '''create table inbox (
      email		char(15),
      msgTimestamp	date,
      sender	char(15),
      content	text,
      rno		int,
      seen		char(1),
      primary key (email, msgTimestamp),
      foreign key (email) references members,
      foreign key (sender) references members,
      foreign key (rno) references rides
    );'''

    cursor.execute(members_Table)
    cursor.execute(cars_Table)
    cursor.execute(locations_Table)
    cursor.execute(rides_Table)
    cursor.execute(bookings_Table)
    cursor.execute(enroute_Table)
    cursor.execute(requests_Table)
    cursor.execute(inbox_Table)
    connection.commit()

    return

# Show messages associated with paricular email
def show_messages(email):
    print()

# Login with email & password
def login():
    print()
    val = 0
    while val == 0:
        in_members = 0
        print("Login")
        print("Enter email:")
        email = input()
        print("Enter password:")
        password = input()
        data = (email,password)
        cursor.execute('SELECT count(*) FROM members WHERE email=? and pwd=?;', data)
        in_members = cursor.fetchone()
        if  in_members[0] == 1:
            print("Login successful")
            show_messages(email)
            val = 1
        elif in_members[0] == 0:
            print("Invalid email/password")
    return

# Register new & unique email
def register():
    print("Register")
    val = 0
    while val == 0:
        print()
        print("Enter new email:")
        email = input()
        data = (email,)
        cursor.execute('SELECT count(*) FROM members WHERE email=?', data)
        in_members = cursor.fetchone()
        if  in_members[0] == 0:
            val = 1
            print("Enter name:")
            name = input()
            print("Enter phone:")
            phone = input()
            print("Enter password:")
            password = input()
            data = (email,name,phone,password)
            cursor.execute('INSERT INTO members (email, name, phone, pwd) VALUES (?,?,?,?);', data)
            login()
        elif in_members[0] == 1:
            print("Email already registered")

# Login / Register Options
def startscreen():
    val = 0
    while val == 0:
        print("1. Login")
        print("2. Register")
        opt = int(input())
        if opt == 1 :
            val = 1
            login()
        elif opt == 2:
            val = 1
            register()
        else:
            print("Invalid option. Choose 1 or 2")
def main():
    global connection, cursor

    path="./register.db"
    connect(path)
    drop_tables()
    define_tables()
    startscreen()

if __name__ == "__main__":
    main()
