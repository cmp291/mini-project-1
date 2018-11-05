import sqlite3
import time
import sys
import hashlib
import datetime
import getpass

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
      rno		integer primary key autoincrement,
      price		int,
      rdate		date,
      seats		int,
      lugDesc	char(10),
      src		char(5),
      dst		char(5),
      driver	char(15),
      cno		int,
      
      foreign key (src) references locations,
      foreign key (dst) references locations,
      foreign key (driver) references members,
      foreign key (cno) references cars
    );'''
    bookings_Table = '''create table bookings (
      bno		integer primary key autoincrement,
      email		char(15),
      rno		int,
      cost		int,
      seats		int,
      pickup	char(5),
      dropoff	char(5),
     
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

def insert_values():
    #-- Data originally prepared by Tanner Chell, tchell@ualberta.ca,
    #-- published on 2018-Oct-05
    #-- modified by Nicholas Leong, nleong1@ualberta.ca for miniProject 1

    #-- |email|name|phone|pwd|
    insert_members = '''insert into members values
            ('jane_doe@abc.ca', 'Jane Maria-Ann Doe', '780-342-7584', 'jpass'),
            ('bob@123.ca', 'Bob Williams', '780-342-2834', 'bpass'),
            ('maria@xyz.org', 'Maria Calzone', '780-382-3847', 'mpass'),
            ('the99@oil.com', 'Wayne Gretzky', '780-382-4382', 'tpass'),
            ('connor@oil.com', 'Connor Mcdavid', '587-839-2838', 'cpass'),
            ('don@mayor.yeg', 'Don Iveson', '780-382-8239', 'dpass'),
            ('darryl@oil.com', 'Darryl Katz', '604-238-2380', 'dpass'),
            ('reilly@esks.org', 'Mike Reilly', '780-389-8928', 'rpass'),
            ('mess@marky.mark', 'Mark Messier', '516-382-8939', 'mpass'),
            ('mal@serenity.ca', 'Nathan Fillion', '780-389-2899', 'mpass'),
            ('kd@lang.ca', 'K. D. Lang', '874-384-3890', 'kpass'),
            ('nellie@five.gov', 'Nellie McClung', '389-930-2839', 'npass'),
            ('marty@mc.fly', 'Micheal J. Fox', '780-382-3899', 'mpass'),
            ('cadence@rap.fm', 'Roland Pemberton', '780-938-2738', 'cpass'),
            ('john@acorn.nut', 'John Acorn', '780-389-8392', 'jpass');'''

    #-- |cno|make|model|year|seats|owner|
    insert_cars = '''insert into cars values
            (1, 'Honda', 'Civic', 2010, 4, 'jane_doe@abc.ca'),
            (2, 'Ford', 'E-350', 2012, 15, 'bob@123.ca'),
            (3, 'Toyota', 'Rav-4', 2016, 4, 'don@mayor.yeg'),
            (4, 'Subaru', 'Forester', 2017, 4, 'reilly@esks.org'),
            (5, 'Ford', 'F-150', 2018, 4, 'connor@oil.com'),
            (6, 'Ram', '2500', 2017, 4, 'mess@marky.mark'),
            (7, 'Toyota', 'Matrix', 2007, 4, 'maria@xyz.org'),
            (8, 'Dodge', 'Caravan', 2013, 6, 'mess@marky.mark'),
            (9, 'Ford', 'Flex', 2011, 4, 'maria@xyz.org'),
            (10, 'Volkswagon', 'Vanagon', 1974, 5, 'the99@oil.com'),
            (11, 'Toyota', 'Sienna', 2012, 6, 'john@acorn.nut'),
            (12, 'Honda', 'Accord', 2010, 4, 'john@acorn.nut'),
            (13, 'Jeep', 'Wrangler', 2007, 2, 'cadence@rap.fm');'''

    #-- |lcode|city|prov|address|
    insert_locations = '''insert into locations values
            ('cntr1', 'Edmonton', 'Alberta', 'Rogers Place'),
            ('cntr2', 'Edmonton', 'Alberta', 'City Hall'),
            ('sth1', 'Edmonton', 'Alberta', 'Southgate'),
            ('west1', 'Edmonton', 'Alberta', 'West Ed Mall'),
            ('cntr3', 'Edmonton', 'Alberta', 'Tyrell Museum'),
            ('cntr4', 'Edmonton', 'Alberta', 'Citadel Theater'),
            ('cntr5', 'Edmonton', 'Alberta', 'Shaw Center'),
            ('sth2', 'Edmonton', 'Alberta', 'Black Dog'),
            ('sth3', 'Edmonton', 'Alberta', 'The Rec Room'),
            ('sth4', 'Edmonton', 'Alberta', 'MEC South'),
            ('nrth1', 'Edmonton', 'Alberta', 'MEC North'),
            ('nrth2', 'Edmonton', 'Alberta', 'Rexall Place'),
            ('nrth3', 'Edmonton', 'Alberta', 'Commonwealth'),
            ('nrth4', 'Edmonton', 'Alberta', 'Northlands'),
            ('yyc1', 'Calgary', 'Alberta', 'Saddledome'),
            ('yyc2', 'Calgary', 'Alberta', 'McMahon Stadium'),
            ('yyc3', 'Calgary', 'Alberta', 'Calgary Tower'),
            ('van1', 'Vancouver', 'British Columbia', 'BC Place'),
            ('van2', 'Vancouver', 'British Columbia', 'Rogers Arena'),
            ('sk1', 'Regina', 'Saskatchewan', 'Mosaic Field'),
            ('sk2', 'Saskatoon', 'Saskatchewan', 'Wanuskewin'),
            ('ab1', 'Jasper', 'Alberta', 'Jasper Park Lodge');
            --('van3', 'Abbotsford', 'British Columbia', 'Abbotsford Airport');'''

    #-- |rno|price|rdate|seats|lugDesc|src|dst|driver|cno|
    insert_rides = '''insert into rides values
            (1, 50, '2018-11-01', 4, 'Large Bag', 'cntr1', 'yyc1', 'the99@oil.com', 10),
            (2, 50, '2018-11-05', 4, 'Large Bag', 'yyc1', 'cntr2', 'the99@oil.com', 10),
            (3, 50, '2018-11-30', 4, 'Medium Bag', 'cntr1', 'yyc1', 'mess@marky.mark', 8),
            (4, 30, '2018-11-17', 15, '5 large bags', 'nrth1', 'yyc2', 'bob@123.ca', 2),
            (5, 50, '2018-11-23', 3, 'Backpack', 'cntr2', 'yyc3', 'maria@xyz.org', 7),
            (6, 10, '2018-07-23', 4, 'Medium Bag', 'west1', 'sth4', 'don@mayor.yeg', 3),
            (7, 10, '2018-09-30', 4, 'Medium Bag', 'cntr2', 'cntr3', 'reilly@esks.org', 4),
            (8, 10, '2018-10-11', 4, 'Medium Bag', 'nrth1', 'sth2', 'connor@oil.com', 4),
            (9, 10, '2018-10-12', 4, 'Medium Bag', 'cntr5', 'sth3', 'jane_doe@abc.ca', 1),
            (10, 10, '2018-04-26', 4, 'Medium Bag', 'cntr4', 'cntr2', 'bob@123.ca', 2),
            (11, 100, '2018-08-08', 4, 'Medium Bag', 'cntr1', 'van1', 'mess@marky.mark', 6),
            (12, 100, '2018-05-13', 2, 'Medium Bag', 'sk1', 'van2', 'bob@123.ca', 2),
            (13, 75, '2018-06-11', 3, 'Large Bag', 'yyc1', 'sk2', 'the99@oil.com', 10),
            (14, 10, '2018-10-13', 4, 'Large Bag', 'sth4', 'yyc1', 'reilly@esks.org', 4),
            (15, 15, '2018-10-05', 5, 'Medium Bag', 'nrth4', 'yyc1', 'the99@oil.com', 10),
            (16, 75, '2018-10-03', 2, 'Small Bag', 'yyc3', 'sk2', 'connor@oil.com', 5),
            (17, 150, '2018-10-11', 3, 'Medium Bag', 'sk2', 'van1', 'jane_doe@abc.ca', 1),
            (18, 10, '2018-10-23', 3, 'Large Bag', 'nrth3', 'yyc1', 'don@mayor.yeg', 3),
            (19, 10, '2015-04-22', 4, 'Small Bag', 'cntr1', 'cntr2', 'bob@123.ca', 2),
            (20, 50, '2018-12-11', 1, 'Large Bag', 'cntr2', 'yyc2', 'the99@oil.com', 10),
            (21, 50, '2018-12-12', 1, 'Large Bag', 'cntr2', 'yyc3', 'the99@oil.com', 10),
            (22, 10, '2018-09-13', 1, 'Large Bag', 'cntr2', 'cntr4', 'the99@oil.com', 10),
            (23, 10, '2018-09-14', 1, 'Large Bag', 'cntr2', 'cntr5', 'the99@oil.com', 10),
            (24, 10, '2018-09-15', 1, 'Large Bag', 'cntr2', 'sth1', 'the99@oil.com', 10),
            (25, 10, '2018-09-16', 1, 'Large Bag', 'cntr2', 'sth2', 'the99@oil.com', 10),
            (26, 50, '2018-12-06', 1, 'Large Bag', 'cntr2', 'yyc1', 'bob@123.ca', 2),
            (27, 53, '2018-09-07', 2, 'Large Bag', 'cntr2', 'yyc3', 'bob@123.ca', 2),
            (28, 10, '2018-09-08', 1, 'Large Bag', 'cntr2', 'cntr4', 'bob@123.ca', 2),
            (29, 10, '2018-09-09', 1, 'Large Bag', 'cntr2', 'cntr5', 'bob@123.ca', 2),
            (30, 10, '2018-09-10', 1, 'Large Bag', 'cntr2', 'sth1', 'bob@123.ca', 2),
            (31, 10, '2018-09-11', 1, 'Large Bag', 'cntr2', 'sth2', 'bob@123.ca', 2),
            (32, 10, '2018-09-12', 1, 'Large Bag', 'cntr2', 'sth3', 'bob@123.ca', 2),
            (33, 10, '2018-09-01', 1, 'Large Bag', 'cntr2', 'cntr1', 'don@mayor.yeg', 3),
            (34, 10, '2018-09-02', 1, 'Large Bag', 'cntr2', 'nrth1', 'don@mayor.yeg', 3),
            (35, 10, '2018-09-03', 1, 'Large Bag', 'cntr2', 'cntr3', 'don@mayor.yeg', 3),
            (36, 10, '2018-09-04', 1, 'Large Bag', 'cntr2', 'cntr4', 'don@mayor.yeg', 3),
            (37, 10, '2018-09-05', 1, 'Large Bag', 'cntr2', 'sth1', 'don@mayor.yeg', 3),
            (38, 10, '2018-09-06', 1, 'Large Bag', 'cntr2', 'sth2', 'don@mayor.yeg', 3),
            (39, 10, '2018-09-07', 1, 'Large Bag', 'cntr2', 'sth3', 'don@mayor.yeg', 3),
            (40, 50, '2018-09-08', 1, 'Large Bag', 'cntr2', 'yyc1', 'don@mayor.yeg', 3),
            (41, 100, '2018-11-05', 2, 'Large Bag', 'cntr1', 'sk1', 'don@mayor.yeg', 3),
            (42, 150, '2018-11-05', 2, 'Large Bag', 'van2', 'nrth2', 'don@mayor.yeg', 3),
            (43, 10, '2018-10-14', 4, 'Large Bag', 'sth4', 'yyc1', 'jane_doe@abc.ca', 1);'''

    #-- |bno|email|rno|cost|seats|pickup|dropoff|
    insert_bookings = '''insert into bookings values
            (1, 'connor@oil.com', 1, null, 1, null, null),
            (2, 'connor@oil.com', 2, null, 1, null, null),
            (3, 'kd@lang.ca', 3, 45, 1, 'cntr2', null),
            (4, 'reilly@esks.org', 4, 30, 13, null, null),
            (5, 'don@mayor.yeg', 5, 50, 1, 'cntr2', 'yyc3'),
            (6, 'marty@mc.fly', 18, null, 3, null, null),
            (7, 'darryl@oil.com', 20, null, 1, null, null),
            (8, 'john@acorn.nut', 26, null, 1, null, null),
            (9, 'cadence@rap.fm', 27, null, 1, null, null),
            (10, 'connor@oil.com', 5, 45, 1, null, null),
            (11, 'mal@serenity.ca', 41, null, 1, null, null),
            (12, 'nellie@five.gov', 42, null, 1, null, null);'''

    #-- |rno|lcode|
    insert_enroute = '''insert into enroute values
            (12, 'yyc1'),
            (16, 'sk1'),
            (17, 'cntr2');'''

    # -- |rid|email|rdate|pickup|dropoff|amount|
    insert_requests = '''insert into requests values
            (1, 'darryl@oil.com', '2018-07-23', 'nrth1', 'cntr1', 10),
            (2, 'nellie@five.gov', '2018-07-22', 'west1', 'sth4', 10),
            (3, 'mal@serenity.ca', '2018-10-11', 'nrth2', 'sth3', 10),
            (4, 'don@mayor.yeg', '2018-10-11', 'nrth2', 'sth3', 10),
            (5, 'the99@oil.com', '2018-10-11', 'nrth1', 'ab1', 10),
            (6, 'marty@mc.fly', '2018-10-11', 'sk1', 'sth3', 10),
            (7, 'mess@marky.mark', '2018-10-11', 'nrth2', 'sth3', 1),
            (8, 'mess@marky.mark', '2018-10-11', 'nrth2', 'sth3', 100),
            (9, 'jane_doe@abc.ca', '2018-04-26', 'cntr3', 'cntr2', 10);'''

     # -- |email|msgTimestamp|sender|content|rno|seen|
    insert_inbox = '''insert into inbox values
            ('don@mayor.yeg', '2018-08-04', 'darryl@oil.com', 'message content is here', 36, 'n'),
            ('jane_doe@abc.ca', '2018-09-04', 'darryl@oil.com', '2nd message content is here', 43, 'n'),
            ('don@mayor.yeg', '2018-10-04', 'darryl@oil.com', '3rd message content is here', 42, 'n');
            '''
    cursor.execute(insert_members)
    cursor.execute(insert_rides)
    cursor.execute(insert_cars)
    cursor.execute(insert_enroute)
    cursor.execute(insert_requests)
    cursor.execute(insert_inbox)
    cursor.execute(insert_bookings)
    cursor.execute(insert_locations)
    connection.commit()
    return

# Show options menu
def show_menu(email):
    while True:
        print("\n\n1.Offer a ride")
        print("2.Search for rides")
        print("3.Book members or cancel bookings")
        print("4.Post ride requests")
        print("5.Search and delete ride requests")
        print("Enter Log out to exit ")
        choice = input("Select an option: ")
        choice.lower()
        if choice == "log out":
            print("Log out successfully\n")
            startscreen()
        else:
            choice = int(choice)
            if choice == 1:
                offer_a_ride(email)
            if choice == 2:
                search_for_rides(email)
            if choice == 4:
                post_ride_requests(email)
            if choice == 3:
                bookmembers_cancelbookings(email)

# Show messages associated with paricular email
def show_messages(email):
    print("Unread Messages")
    data = (email,)
    get_messages = ''' SELECT sender, content, msgTimestamp FROM inbox WHERE ? = email AND seen = 'n';
    '''
    cursor.execute(get_messages,data)
    messages = cursor.fetchone()
    print(messages)
    set_seen = '''UPDATE inbox SET seen = 'y' WHERE ? = email;
    '''
    cursor.execute(set_seen,data)
    connection.commit()
    show_menu(email)


    


def check_location(locode):

#This function is used to return a location code,
# if it is not a location code, your system should return all locations that have the keyword as a substring in city, province or address fields
# If there are more than 5 matching locations, at most 5 matches will be shown at a time, letting the member select a location or see more matches.

    lcd = (locode,)
    # try to find the matched location code
    try:
        cursor.execute('select lcode from locations where lower(lcode) = ?',lcd)
        result = cursor.fetchone()
        if result is not None:
            return result[0]
    except:
        print("Error in sql 2")

    # try to find the matched substrings in city , prov, address
    try:
        find_substring = '''select lcode ,city, prov, address from locations
        where lower(locations.city) like '%{}%' or lower(locations.prov) like '%{}%' or lower(locations.address) like '%{}%' 
        '''.format(locode,locode, locode)
        
        
        cursor.execute(find_substring)
        result = cursor.fetchall()
        

        if not result:
            sys.exit("Error in reading in location")
        print(len(result))
        
        while True:
            for iterm in range(0, len(result)):

                
                # after showing the first five elements, let user select
                if iterm != 0 and iterm%5 == 0 :
                    
                    choose = input("Select a location code or enter 1 to see more matches: ")
                    if choose != "1":
                        return choose
                    print(result[iterm])
        
                else:
                    print(result[iterm], ',')
            
            choose = input("Select a location code or enter 1 to see more matches: ")
            if choose != "1":
                return choose

    except Exception as e:
        print("Error in sql 3",str(e))


def get_carnumber(email):

    #Try to get the car number if the user enters
    
    while True:
    
        carno = input("Please enter the car number(optional). Enter pass to enter a escape. Enter 'Log out' if you want to quit: ")

        #log out option
        if carno == 'log out':
            print("Log out successfully")
            startscreen()

        #if the user enters a car number, check its belonger. If it is correct, store the car number. Otherwise print error message
        if carno == "pass":
            return None
        
        else:
            try:
                find_car = '''select email from members, cars where lower(members.email) = lower(cars.owner) and cars.cno = {}'''.format(carno)
                
                cursor.execute(find_car)               
                result = cursor.fetchall()
            
                if result != email:
                    print("Sorry. This car does not belong to you")
                else:
                    return carno

            except:
                print("Error in offeraride")



def get_seatsno():
    # Try to get the number of seats from stdin
    while True:
        
        noseats = input("Please enter the number of seats offered. Enter 'Log out' if you want to quit: ")

        noseats.lower()
        if noseats == 'log out':
            print("Log out successfully")
            startscreen()

        if noseats.isdigit():
            noseats = int(noseats)
            return noseats

        else:
            print ("Invaild number")


def get_price():
# Try to get the correct price from stdin
    while True:
    
        price = input("Please enter the price per seat,Enter 'Log out' if you want to quit:")

        price.lower()
        
        if price == 'log out':
            print("Log out successfully")
            startscreen()

        if price.isdigit():
            price = int(price)
            return price
        else:
            print ("Invaild price ")


def get_date():
#Try to get the date    
    while True :
        date = input("Please enter the date by using format year-month-day.Enter 'Log out' if you want to quit: ")
        date.lower()

        if date == 'log out':
            print("Log out successfully")
            startscreen()
        
        else:
            try:
                datetime.datetime.strptime(date, '%Y-%m-%d')
                return date
        
            except:
                print("Invaild date. Please try again. ")
        

def get_luagge():
    
    luggage_description = input("Please enter a luggage description. Enter 'Log out' if you want to quit: ")

    luggage_description.lower()
    
    if luggage_description == 'log out':
        print("Log out successfully")
        startscreen()

    else:
        return luggage_description

        

def offer_a_ride(email):

    carno = get_carnumber(email)

    noseats = get_seatsno()

    price = get_price()

    date = get_date()

    luggage_description = get_luagge()

    #Try to get source location and destination location from user
    while True:
        sourcelo = input("Please enter a source location. Enter 'Log out' if you want to quit: ")
    
        sourcelo.lower()
        
        if sourcelo == 'log out':
            print("Log out successfully")
            startscreen()

        else:
            return_sourcelo = check_location(sourcelo)
            print (return_sourcelo)

        destinationlo = input("Please enter a destination location. Enter 'Log out' if you want to quit: ")

        destinationlo.lower()

        if destinationlo == 'log out':
            print("Log out successfully")
            startscreen()

        else:
            returndestinationlo = check_location(destinationlo)
            print(returndestinationlo)
            break
    

    

        
    # Update the rides table
    data = (price, date, noseats, luggage_description, return_sourcelo, returndestinationlo,email, carno)

    cursor.execute( '''insert into rides(price, rdate, seats, lugDesc, src, dst, driver, cno) values (?,?,?,?,?,?,?,?) ''', data)
    connection.commit()
    rno = cursor.lastrowid
   

    while True:
        
        enlcode = input("Please enter an enroute location(optinal). Note: you are only allowed to enter one enroute location each time. Enter pass if you want to escape. Enter 'Log out' if you want to quit: ")
        
        enlcode.lower()

        if enlcode == 'log out':
            print("Log out successfully")
            startscreen()
        
        if enlcode == "pass":
            break
        
        else:
            renlcode = check_location(enlcode)
            data_enroute = (rno, renlcode)
            cursor.execute('''insert into enroute(rno, lcode) values (?,?)''', data_enroute)
            connection.commit
        
    print("Offered a ride successfully ")





def post_ride_requests(email):
    
    date = get_date()
    
    #Try to get providing a date, a pick up location code, a drop off location code
    while True:
        pickup_lcode = input("Please provide a pick up location code. Enter Log out to exit: ")
        
        if pickup_lcode == "Log out":
            sys.exit("Log out successfully.")
        
        else:
            return_pickl = check_location(pickup_lcode)


        dropoff_lcode = input("Please provide a drop off location code. Enter Log out to exit: ")
        
        if dropoff_lcode == "Log out":
            sys.exit("Log out successfully.")
        
        else:
            return_dropl = check_location(dropoff_lcode)
            break

        
    # Try to get and the amount willing to pay per seat.
    while True:
        
        amount = input("Please enter the amount willing to pay per seat. Enter Log out to exit: ")
        
        if pickup_lcode == "Log out":
            sys.exit("Log out successfully.")
        
        if amount.isdigit():
            amount = int(amount)
            break
        
        else: 
            print("Invaild amount.")

    #Update the request table

    data = (email, date, return_pickl, return_dropl, amount)
    cursor.execute(''' insert into requests(email, rdate, pickup, dropoff, amount) values (?,?,?,?,?)''',data)
    connection.commit()

    print("Made a request successfully ")




def bookaride():

    email = input("Please  enter the  driver's email to book rides which is offered by this driver. Enter Log out to exit: :")

    if email == "Log out":
        sys.exit("Log out successfully.")
    
    




def bookmembers_cancelbookings(email):

    while True:

        choice = input("Enter 1 to see all bookings on rides you offers.\nEnter 2 if you want to cancel any booking.\nEnter 3 to book a ride.\nEnter Log out to exit: ")
    
        choice.lower()

        if choice == "log out":
           print("Log out successfully.")
           startscreen()

    
        if choice == "1":
            listbookings(email)

        elif choice == "2":
            cancelbooking(email)
        
        elif choice == "3":
            bookaride()
            


def sendmessage(no, sender, flag):

    print(no)

    cursor.execute('''SELECT datetime('now');''')
    result = cursor.fetchone()
    date = result[0]
    
    #Send message to members whose bookings are cancelled 
    if (flag == 1):
    
        try:
            cursor.execute('''select email from bookings where bno = ?;''',no)
            reciver_email = cursor.fetchone()
            reciver = reciver_email[0]

            cursor.execute('''select rno from bookings where bno = ?;''',no)
            result = cursor.fetchone()
            rno = result[0]

            data = (reciver, date , sender, "Your booking has been cancelled.", rno, "n")

            cursor.execute(''' insert into inbox(email, msgTimestamp, sender, content, rno, seen) values (?, ?, ?, ?, ?, ?)''', data)

            connection.commit()

        except Exception as e:
            print("Error in sql 1" + str(e))


    if (flag == 2):

        try:
            cursor.execute('''select driver from rides where rno = ?;''',no)
            reciver_email = cursor.fetchone()
            reciver = reciver_email[0]

            data = (reciver, date , sender, "I want to book the ride that you offer.", no[0], "n")

            cursor.execute(''' insert into inbox(email, msgTimestamp, sender, content, rno, seen) values (?, ?, ?, ?, ?, ?)''', data)

            connection.commit()

        except Exception as e:
            print("Error in sql 2 " + str(e))


def cancelbooking(email):

    #First list all the bookings, then let users enter the bno which they want to delete
    listbookings(email)
    
    cancelbno = input("Please enter the bno which you want to cancel. Note: you are only allowed to cancel one bno each time. Enter Log out to exit: ")

    cancelbno.lower()
    if cancelbno == "log out":
        print("Log out successfully.")
        startscreen()
    
    if not cancelbno.isdigit():
        print("Invaild bno. Please try again")
    
    else:

        bno = int(cancelbno)
        b = (bno,)
        #send messages to whose booking is deleted
        sendmessage(b, email,1)
        cursor.execute('''delete from bookings where bno = ? ;''', b)
        connection.commit()
        print("Delete it successfully.")
        

    


def listbookings(email):

#List all bookings that the user offers
    email1 = (email,)
    

    try:
        cursor.execute(''' select bno, email, rno, cost, seats, pickup, dropoff from bookings  
        where rno = (select rno from rides where lower(rides.driver) = ? );''', email1)
        results = cursor.fetchall()
        
    
        if len(results):
            for iterm in results:
                print(iterm)
            print("\n")
   
        else:
            print("There are no bookings on rides you offer.\n")

    except:
        print("Error in sql 3")
    





def search_for_rides(email):
    get_input(email)
    search_for_locations(keywords_list,email)
   
    
def get_input(email):
    
    while True:
        user_input = input("Enter 1~3 keywords separate by one space, Enter 'Log out' if you want to quit: ")
    
        user_input.lower()
    
        if  user_input == "log out":
            print("Log out successfully.")
            startscreen() 
    
    
        keywords_list = user_input.split(' ')
    
        # to eliminate the possibility that the user may enter NULL
        # returns a list of keywords
        keywords_list[:] = [item for item in keywords_list if item != '']
        
        search_for_locations(keywords_list,email)





def search_for_locations(keywords, email):     

    total_output = []

    if (len(keywords) == 1):
        lcd = (keywords[0],)
        try:
            lcd = (keywords[0],)
            cursor.execute('''select lcode from locations where lower(locations.lcode) = ? ''',lcd)
            result = cursor.fetchone()


        except Exception as e:
                print("Error in sql 3",str(e))

        if not result:
            try:
                find_substring = '''select lcode from locations where lower(locations.lcode) like '%{}%' or lower(locations.city) like '%{}%' or lower(locations.prov) like '%{}%' or lower(locations.address) like '%{}%'
                '''.format(keywords[0],keywords[0],keywords[0],keywords[0])
        
                cursor.execute(find_substring)
                result = cursor.fetchall()
    
            except Exception as e:
                print("Error in sql 4",str(e))

        if not result:
            print("There are no matching rides.\n")

        
    elif (len(keywords) == 2):
        
        try:
            
            find_substring = '''select lcode from locations where lower(locations.city) like '%{}%' or lower(locations.city) like '%{}%' and lower(locations.prov) like '%{}%' or  
                lower(locations.prov) like '%{}%' and lower(locations.address) like '%{}%' or lower(locations.address) like '%{}%' 
                '''.format(keywords[0],keywords[1],keywords[0],keywords[1],keywords[0],keywords[1])
            
            cursor.execute(find_substring)
            result=cursor.fetchall() 
            
        except Exception as e:
                print("Error in sql 4",str(e))
    
    
    # try to find the matched location code
    
    
    elif (len(keywords) == 3):

        try:

            find_substring = '''select lcode from locations where lower(locations.city) like '%{}%' or lower(locations.city) like '%{}%' or lower(locations.city) like '%{}%' and lower(locations.prov) like '%{}%' or  
                lower(locations.prov) like '%{}%' or lower(locations.prov) like '%{}%' and lower(locations.address) like '%{}%' or lower(locations.address) like '%{}%' or lower(locations.address) like '%{}%'
                '''.format(keywords[0],keywords[1],keywords[2],keywords[0],keywords[1],keywords[2],keywords[0],keywords[1],keywords[2],)

            cursor.execute(find_substring)
            result=cursor.fetchall() 
    
        except Exception as e:
                print("Error in sql 4",str(e))
    
    
    for iterm in result:
                
        try:
            cursor.execute(''' select * from rides r left outer join cars c on (r.cno = c.cno) where lower(src)=? or lower(dst)=?''', (iterm[0],iterm[0]))
            output1 = cursor.fetchall() 
            list(output1)
            total_output = total_output + output1
             
        except Exception as e:
            print("Error in sql 4",str(e))
        
        
    if not total_output:
        print("There are no matching rides\n")
        
    for i in range(0, len(total_output)):
                
            if i != 0 and i%5 == 0 :
                
                user_enter = input("\nEnter 'a' to see more options; Enter pass if you do not want to select any ride; Enter its rno if you want to select a ride;Enter Log out to quit:")
                user_enter.lower()
                if (user_enter == "log out"):
                    print("Log out successfully.")
                    startscreen()
                
                elif (user_enter == "a"):
                    print(total_output[i],'\n')
                
                elif(user_enter.isdigit()):
                    sendmessage( (int(user_enter),), email, 2)
                    break

                elif(user_enter == "pass"):
                    return

                else:
                    sys.exit("Error in reading in user inputs.\n")
    
            else:
                print(total_output[i],'\n')
        
        
    choice = input("\nEnter its rno if you want to select a ride; Enter pass if you do not want to select any ride. Enter Log out to quit:")
    choice.lower()
    
    if (choice == "log out"):
        print("Log out successfully.")
        startscreen()
    
    elif(choice == "pass"):
        return

    elif choice.isdigit():
        sendmessage((int(choice),),email,2)

    else:
        print("Invaild rno")


            
            
            
            
            
   
# Login with email & password
def login():
    print()
    val = 0
    while val == 0:
        in_members = 0
        print("Login")
        print("Enter email:")
        email = input()
        email.lower()
    #    print("Enter password:")
        password = getpass.getpass("Enter password:")
        data = (email,password)
        cursor.execute('SELECT count(*) FROM members WHERE lower(email)=? and pwd=?;', data)
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
    insert_values()
    startscreen()

if __name__ == "__main__":
    main()
