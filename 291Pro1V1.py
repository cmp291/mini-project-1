import sqlite3
import time
import sys
import hashlib
import datetime
import getpass
import random

connection = None
cursor = None

def connect():
    global connection, cursor

    connection = sqlite3.connect(sys.argv[1])
    cursor = connection.cursor()
    cursor.execute(' PRAGMA forteign_keys=ON; ')
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
        choice = input("Select an option: ").lower()
        if choice == "log out":
            print("Log out successfully\n")
            startscreen()
        else:
            choice = int(choice)
            if choice == 1:
                offer_a_ride(email)
            elif choice == 2:
                search_for_rides(email)
            elif choice == 3:
                bookmembers_cancelbookings(email)
            elif choice == 4:
                post_ride_requests(email)
            elif choice == 5:
                searchDeleteRideRequests(email)
            else:
                print("Invalid option")
                
# Show messages associated with paricular email
def show_messages(email):
    print("Unread Messages")
    data = (email,)
    get_messages = ''' SELECT sender, content,rno, msgTimestamp FROM inbox WHERE ? = email AND seen = 'n';
    '''
    cursor.execute(get_messages,data)
    messages = cursor.fetchall()
    for msg in messages:
        print(msg)
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

                    choose = input("Select a location code or enter 'a' to see more options: ")
                    if choose != "a":
                        return choose
                    print(result[iterm])
                else:
                    print(result[iterm], ',')
                if iterm == len(result)-1:
                    break
            print("All options have been shown")
            choose = input("Select a location code: ")
            return choose
            break
    except Exception as e:
        print("Error in sql 3",str(e))

def get_carnumber(email):

    #Try to get the car number if the user enters

    while True:

        carno = input("Please enter the car number(optional). Enter pass to enter a escape. Enter 'Log out' if you want to quit: ").lower()

        #log out option
        if carno == 'log out':
            print("Log out successfully")
            startscreen()

        #if the user enters a car number, check its belonger. If it is correct, store the car number. Otherwise print error message
        if carno == "pass":
            return None

        else:
            try:
                carno = int(carno)
                find_car = '''select email from members, cars where lower(members.email) = lower(cars.owner) and cars.cno = {}'''.format(carno)

                cursor.execute(find_car)
                result = cursor.fetchone()[0]

                if result != email:
                    print("Sorry. This car does not belong to you")
                else:
                    return carno

            except:
                print("Error in offeraride")

def get_seatsno():
    # Try to get the number of seats from stdin
    while True:

        noseats = input("Please enter the number of seats offered. Enter 'Log out' if you want to quit: ").lower()
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

        price = input("Please enter the price per seat,Enter 'Log out' if you want to quit:").lower()

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
        date = input("Please enter the date by using format year-month-day.Enter 'Log out' if you want to quit: ").lower()

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

    luggage_description = input("Please enter a luggage description. Enter 'Log out' if you want to quit: ").lower()

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
        sourcelo = input("Please enter a source location. Enter 'Log out' if you want to quit: ").lower()

        if sourcelo == 'log out':
            print("Log out successfully")
            startscreen()

        else:
            return_sourcelo = check_location(sourcelo)
            print (return_sourcelo)

        destinationlo = input("Please enter a destination location. Enter 'Log out' if you want to quit: ").lower()

        if destinationlo == 'log out':
            print("Log out successfully")
            startscreen()

        else:
            returndestinationlo = check_location(destinationlo)
            print(returndestinationlo)
            break

    # Update the rides table
    while True:
        rno = random.randint(0,999)
        cursor.execute('''select count(*) from rides where rno = ?''',(rno,))
        un = cursor.fetchone()[0]
        if un == 0:
            break
    data = (rno,price, date, noseats, luggage_description, return_sourcelo, returndestinationlo,email, carno)
    print(data)

    cursor.execute( '''insert into rides(rno,price, rdate, seats, lugDesc, src, dst, driver, cno) values (?,?,?,?,?,?,?,?,?) ''', data)
    connection.commit()

    while True:

        enlcode = input("Please enter an enroute location(optinal). Note: you are only allowed to enter one enroute location each time. Enter pass if you want to escape. Enter 'Log out' if you want to quit: ").lower()

        if enlcode == 'log out':
            print("Log out successfully")
            startscreen()

        if enlcode == "pass":
            break

        else:
            renlcode = check_location(enlcode)
            data_enroute = (rno, renlcode)
            cursor.execute('''insert into enroute(rno, lcode) values (?,?)''', data_enroute)
            connection.commit()
            break
    print("Offered a ride successfully ")

def post_ride_requests(email):

    date = get_date()

    #Try to get providing a date, a pick up location code, a drop off location code
    while True:
        pickup_lcode = input("Please provide a pick up location code. Enter Log out to exit: ").lower()

        if pickup_lcode == "log out":
            sys.exit("Log out successfully.")

        else:
            return_pickl = check_location(pickup_lcode)


        dropoff_lcode = input("Please provide a drop off location code. Enter Log out to exit: ").lower()

        if dropoff_lcode == "log out":
            sys.exit("Log out successfully.")

        else:
            return_dropl = check_location(dropoff_lcode)
            break


    # Try to get and the amount willing to pay per seat.
    while True:

        amount = input("Please enter the amount willing to pay per seat. Enter Log out to exit: ").lower()

        if pickup_lcode == "log out":
            sys.exit("Log out successfully.")

        if amount.isdigit():
            amount = int(amount)
            break

        else:
            print("Invaild amount.")

    #Update the request table
    while True:
        rid = random.randint(0,999)
        cursor.execute('''select count(*) from requests where rid = ?''',(rid,))
        un = cursor.fetchone()[0]
        if un == 0:
            break
    data = (rid,email, date, return_pickl, return_dropl, amount)
    cursor.execute(''' insert into requests(rid,email, rdate, pickup, dropoff, amount) values (?,?,?,?,?,?)''',data)
    connection.commit()

    print("Made a request successfully ")

def listrides(email):
    my_rides_query = '''select  r.rno, r.price, r.rdate, r.lugDesc, r.src, r.dst, r.cno,ifnull(r.seats-b.seats,0) as booked from rides r left outer join bookings b on (b.rno = r.rno)
                where r.driver = ?'''
    cursor.execute(my_rides_query,(email,))
    my_rides = cursor.fetchall()
    while True:
        for iterm in range(0, len(my_rides)):
            # after showing the first five elements, let user select
            if iterm != 0 and iterm%5 == 0 :

                choose = input("Select a ride or enter 'a' to see more rides: ")
                if choose != "a":
                    return choose
                print(my_rides[iterm])
            else:
                print(my_rides[iterm], ',')
            if iterm == len(my_rides)-1:
                break
        print("All options have been shown")
        choose = input("Select a ride: ")
        return choose
        break

def is_a_member(email):
    is_member_query = '''select count(*) from members where email = ?'''
    cursor.execute(is_member_query,(email,))
    is_member = cursor.fetchone()[0]
    if is_member == 0:
        print("Passenger is not a member. Cannot be booked on a ride.")
    return is_member

def bookaride(email):

    ride = listrides(email)
    is_member = 0
    while is_member == 0:
        passenger = input("Please  enter the email of the passenger to be booked on your ride. Enter Log out to exit:").lower()
        if passenger == "log out":
            print("Log out successfully.")
            startscreen()
        else:
            is_member = is_a_member(passenger)
    if is_member == 1:
        cost = get_price()
        seats = get_seatsno()
        available_query = '''select ifnull(r.seats- sum(b.seats),0) from rides r left outer join bookings b on (b.rno = r.rno)
                    where r.driver = ? and r.rno = ? group by r.rno'''
        cursor.execute(available_query,(email,ride))
        available_seats = cursor.fetchone()
        if seats > available_seats[0] :
            proceed = input("Ride will be overbooked if you proceed. Do you wish to proceed ? (yes/no). Enter Log out to exit:").lower()
            if proceed == "log out":
                print("Log out successfully.")
                startscreen
            elif proceed == "no":
                show_menu()
        pickup = input("Enter the pickup location.  Enter Log out to exit:").lower()

        if pickup == 'log out':
            print("Log out successfully")
            startscreen()

        else:
            return_pickup = check_location(pickup)
            print (return_pickup)
        dropoff = input("Enter the dropoff location.  Enter Log out to exit:").lower()

        if dropoff == 'log out':
            print("Log out successfully")
            startscreen()

        else:
            return_dropoff = check_location(dropoff)
            print (return_dropoff)
        while True:
            bno = random.randint(0,999)
            cursor.execute('''select count(*) from bookings where bno = ?''',(bno,))
            un = cursor.fetchone()[0]
            if un == 0:
                break
        new_booking =(bno,passenger,ride,cost,seats,pickup,dropoff)
        print(new_booking)
        sendmessage(passenger,email,ride,"You have been booked on a ride.")
        cursor.execute('''INSERT INTO bookings(bno,email, rno, cost, seats, pickup, dropoff) VALUES (?,?, ?, ?, ?, ?, ?) ''',new_booking)
        connection.commit()
        print("ride booked")

def bookmembers_cancelbookings(email):

    while True:
        choice = input("Enter 1 to see all bookings on rides you offers.\nEnter 2 if you want to cancel any booking.\nEnter 3 to book a ride.\nEnter Log out to exit: ").lower()

        if choice == "log out":
           print("Log out successfully.")
           startscreen()

        if choice == "1":
            listbookings(email)

        elif choice == "2":
            cancelbooking(email)

        elif choice == "3":
            bookaride(email)

def sendmessage(receiver, sender,rno,message):

    #Send message to members whose bookings are cancelled
    try:
        cursor.execute('''SELECT datetime('now');''')
        result = cursor.fetchone()
        date = result[0]

        data = (receiver, date , sender, message, rno, "n")

        cursor.execute(''' insert into inbox(email, msgTimestamp, sender, content, rno, seen) values (?, ?, ?, ?, ?, ?)''', data)

        connection.commit()
        print("Message Sent")

    except Exception as e:
        print("Error in sql " + str(e))

def cancelbooking(email):

    #First list all the bookings, then let users enter the bno which they want to delete
    listbookings(email)

    cancelbno = input("Please enter the bno which you want to cancel. Note: you are only allowed to cancel one bno each time. Enter Log out to exit: ").lower()
    if cancelbno == "log out":
        print("Log out successfully.")
        startscreen()

    if not cancelbno.isdigit():
        print("Invaild bno. Please try again")

    else:

        bno = int(cancelbno)
        b = (bno,)
        cursor.execute('''select email from bookings where bno = ?;''',b)
        reciver_email = cursor.fetchone()
        receiver = reciver_email[0]

        cursor.execute('''select rno from bookings where bno = ?;''',b)
        result = cursor.fetchone()
        rno = result[0]
        #send messages to whose booking is deleted
        sendmessage(receiver, email,rno,"Your booking has been cancelled.")
        cursor.execute('''delete from bookings where bno = ? ;''', b)
        connection.commit()
        print("Delete it successfully.")

def listbookings(email):

#List all bookings that the user offers
    email1 = (email,)

    try:
        cursor.execute(''' select b.bno, b.email, b.rno, b.cost, b.seats, b.pickup, b.dropoff from bookings b ,rides r
         where b.rno = r.rno and lower(r.driver) = ?;''', email1)
        results = cursor.fetchall()

        if len(results):
            for iterm in results:
                print(iterm)
            print("\n")

        else:
            print("There are no bookings on rides you offer.\n")

    except:
        print("Error in sql 3")

def listMyRideRequests(email):
    my_request_query = '''select * from requests where email = ? '''
    cursor.execute(my_request_query,(email,))
    my_requests = cursor.fetchall()
    if not my_requests:
        print("None")
    else:
        for req in my_requests:
            print(req)
    return

def cancelRequest(email):
    listMyRideRequests(email)
    del_req = input("Enter the rid of the request you wish to delete. Enter Log out to exit:").lower()
    if del_req == "log out":
       print("Log out successfully.")
       startscreen()
    if not del_req.isdigit():
        print("Invaild rid. Please try again")

    else:
        rid = int(del_req)
        r = (rid,)
        cursor.execute('''delete from requests where rid = ? ;''', r)
        connection.commit()
        print("Deleted successfully.")

def listMatchingRequests(entry,email):
    matches_query = '''select rid, email, rdate, pickup, dropoff, amount from requests r left outer join locations l on ((pickup = lcode) or (dropoff = lcode))
     where lower(lcode) = ? or lower(city)  = ? group by rid'''
    cursor.execute(matches_query,(entry,entry))
    matches = cursor.fetchall()
    if not matches:
        print("No requests matching keyword")
        searchRequests(email)
    else:
        while True:
            for iterm in range(0, len(matches)):
                # after showing the first five elements, let user select
                if iterm != 0 and iterm%5 == 0 :

                    choose = input("Select a request or enter 'a' to see more requests: ")
                    if choose != "a":
                        return choose
                    print(matches[iterm])
                else:
                    print(matches[iterm], ',')
                if iterm == len(matches)-1:
                    break
            print("All options have been shown")
            choose = input("Select a request: ")
            return choose
            break

def searchRequests(email):
    entry = input("Enter a location code or a city. Enter Log out to exit: ").lower()
    if entry == "log out":
       print("Log out successfully.")
       startscreen()
    else:
        choice = listMatchingRequests(entry,email)
        opt = input("Do you want to message the posting member of this request ? (yes/no).Enter Log out to exit: ").lower()
        if opt == "log out":
           print("Log out successfully.")
           startscreen()
        elif opt == "no":
            show_menu(email)
        elif opt == "yes":
            cursor.execute('''select email from requests where rid = ?''',(choice,))
            poster = cursor.fetchone()[0]
            message = input("What do you want to tell posting member of this request ?.")
            sendmessage(poster,email,choice,message)

def searchDeleteRideRequests(email):
    choice = input("Enter 1 to see all your ride requests.\nEnter 2 if you want to delete any request.\nEnter 3 Search ride requests.\nEnter Log out to exit: ").lower()
    if choice == "log out":
       print("Log out successfully.")
       startscreen()

    if choice == "1":
        listMyRideRequests(email)

    elif choice == "2":
        cancelRequest(email)

    elif choice == "3":
        searchRequests(email)

def search_for_rides(email):
    while True:
        user_input = input("Enter 1~3 keywords separate by one space, Enter 'Log out' if you want to quit: ").lower()

        if  user_input == "log out":
            print("Log out successfully.")
            startscreen()

        keywords_list = user_input.split(' ')

        # to eliminate the possibility that the user may enter NULL
        # returns a list of keywords
        keywords_list[:] = [item for item in keywords_list if item != '']
        search_for_locations(keywords_list,email)

def search_for_locations(keywords, email):
    if len(keywords) == 1:
        try:
            cursor.execute('select lcode from locations where lower(lcode) = ?',(keywords[0],))
            result = cursor.fetchone()
            if result is not None:
                ride = result[0]
        except:
            print("Error in sql 2")

        # try to find the matched substrings in city , prov, address
        try:
            find_substring = '''select lcode from locations
            where lower(locations.city) like '%{}%' or lower(locations.prov) like '%{}%' or lower(locations.address) like '%{}%'
            '''.format(keywords[0],keywords[0],keywords[0])

            cursor.execute(find_substring)
            result = cursor.fetchall()
            ride = list(result)
            if not result:
                sys.exit("Error in reading in location")
        except Exception as e:
            print("Error in sql 3",str(e))

    if len(keywords) == 2:
        try:
            cursor.execute('select lcode from locations where lower(lcode) = ? or lower(lcode) = ? ',(keywords[0],keywords[1]))
            result = cursor.fetchone()
            if result is not None:
                ride = result[0]
        except:
            print("Error in sql 2")

        # try to find the matched substrings in city , prov, address
        try:
            find_substring = '''select lcode from locations where ((lower(locations.city) like '%{}%' or lower(locations.city) like '%{}%')  and ((lower(locations.prov) like '%{}%' or
                      lower(locations.prov) like '%{}%') or (lower(locations.address) like '%{}%' or lower(locations.address) like '%{}%')))
                      or  ((lower(locations.prov) like '%{}%' or lower(locations.prov) like '%{}%')  and ((lower(locations.city) like '%{}%' or
                                lower(locations.city) like '%{}%') or (lower(locations.address) like '%{}%' or lower(locations.address) like '%{}%')))
                      or  ((lower(locations.address) like '%{}%' or lower(locations.address) like '%{}%')  and ((lower(locations.prov) like '%{}%' or
                                lower(locations.prov) like '%{}%') or (lower(locations.city) like '%{}%' or lower(locations.city) like '%{}%')))
                      '''.format(keywords[0],keywords[1],keywords[0],keywords[1],keywords[0],keywords[1],keywords[0],keywords[1],keywords[0],keywords[1],keywords[0],keywords[1]
                                 ,keywords[0],keywords[1],keywords[0],keywords[1],keywords[0],keywords[1])
            cursor.execute(find_substring)
            result = cursor.fetchall()
            ride = list(result)
            if not result:
                sys.exit("Error in reading in location")
        except Exception as e:
            print("Error in sql 3",str(e))

    if len(keywords) == 3:
        try:
            cursor.execute('select lcode from locations where lower(lcode) = ? or lower(lcode) = ? or lower(lcode) = ?',(keywords[0],keywords[1],keywords[2]))
            result = cursor.fetchone()
            if result is not None:
                ride = result[0]
        except:
            print("Error in sql 2")

        # try to find the matched substrings in city , prov, address
        try:
            find_substring = '''select lcode from locations where (lower(locations.city) like '%{}%' or lower(locations.city) like '%{}%' or lower(locations.city) like '%{}%')
                      and (lower(locations.prov) like '%{}%' or lower(locations.prov) like '%{}%' or lower(locations.prov) like '%{}%')
                      and (lower(locations.address) like '%{}%' or lower(locations.address) like '%{}%' or lower(locations.address) like '%{}%')
                      '''.format(keywords[0],keywords[1],keywords[2],keywords[0],keywords[1],keywords[2],keywords[0],keywords[1],keywords[2])
            cursor.execute(find_substring)
            result = cursor.fetchall()
            ride = list(result)
            if not result:
                sys.exit("Error in reading in location")
        except Exception as e:
            print("Error in sql 3",str(e))
    opt = input("Do you want to message the posting member of this ride ? (yes/no).Enter Log out to exit: ").lower()
    if opt == "log out":
       print("Log out successfully.")
       startscreen()
    elif opt == "no":
        show_menu(email)
    elif opt == "yes":
        cursor.execute('''select driver from rides where rno = ?''',(ride,))
        poster = cursor.fetchone()[0]
        message = input("What do you want to tell posting member of this request ?.")
        sendmessage(poster,email,ride,message)

def list(result):
    for r in result:
        matching_rides_query = '''select r.rno, r.price, r.rdate, r.seats, r.lugDesc, r.src, r.dst, r.driver, r.cno, c.make, c.model, c.year, c.seats, c.owner
        from rides r left outer join cars c on (r.cno = c.cno) where lower(src)=? or lower(dst)=?'''
        cursor.execute(matching_rides_query,(r[0],r[0]))
        matching_rides = cursor.fetchall()
        print(len(matching_rides))
        while True:
            for iterm in range(0, len(matching_rides)):
                # after showing the first five elements, let user select
                if iterm != 0 and iterm%5 == 0 :

                    choose = input("Select a ride or enter 'a' to see more rides: ")
                    if choose != "a":
                        return choose
                    print(matching_rides[iterm])
                else:
                    print(matching_rides[iterm], ',')
                if iterm == len(matching_rides)-1:
                    break
            print("All options have been shown")
            choose = input("Select a ride: ")
            return choose
            break

# Login with email & password
def login():
    print()
    val = 0
    while val == 0:
        in_members = 0
        print("Login")
        print("Enter email:")
        email = input().lower()
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

    connect()
    startscreen()

if __name__ == "__main__":
    main()
