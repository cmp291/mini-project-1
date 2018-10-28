import sqlite3
import sys
conn = sqlite3.connect(":register.db")
cursor = conn.cursor()


def check_location(locode):

#This function is used to return a location code,
# if it is not a location code, your system should return all locations that have the keyword as a substring in city, province or address fields
# If there are more than 5 matching locations, at most 5 matches will be shown at a time, letting the member select a location or see more matches.


    # try to find the matched location code
    try:
        cursor.execute('select lcode from locations where locations.lcode = ?',locode)
        result = cursor.fetchall()
        if result is not None:
            return result


    except:
        print("Error in sql 2")

    # try to find the matched substrings in city , prov, address
    try:
        cursor.execute('select city from locations where city like %?%', locode)
        resultcity = cursor.fetchall()
        cursor.execute('select prov from locations where prov like %?%', locode)
        resultprov = cursor.fetchall()
        cursor.execute('select address from locations where address like %?%', locode)
        resultadd = cursor.fetchall()

        totalresult = resultcity + resultprov + resultadd

        if not totalresult:
            sys.exit("Error in reading in location")

        while True:

            for iterm in range(0, len(totalresult)):

                # after showing the first five elements, let user select
                if iterm == 5:
                    choose = input("Select a location or enter 1 to see more matches")
                    if choose != 1:
                        return choose

                print(totalresult[iterm], ',')


    except:
        print("Error in sql 3")





def offeraride(email):

    entered1 = input("Please enter the car number(optional) Enter 'Log out' if you want to quit:")

#log out option
    if entered1 == 'Log out':
        sys.exit("Log out successfully")

#if the user enters a car number, check its belonger
    if entered1 is not None:
        try:
            cursor.execute('select email from members, cars where members.email = cars.owner and cars.cno = ？；',entered1)
            result = cursor.fetchall()
            if result != email:
                print("Sorry. This car does not belong to you")

        except:
            print("Error in offeraride")


    noseats = input("Please enter the number of seats offered. Enter 'Log out' if you want to quit: ")

    if noseats == 'Log out':
        sys.exit("Log out successfully")

    noseats = int(noseats)


    price = input("Please enter the price per seat,Enter 'Log out' if you want to quit:")

    if price == 'Log out':
        sys.exit("Log out successfully")

    price = int(price)


    date = input("Please enter the date by using format year-month-day.Enter 'Log out' if you want to quit: ")

    if date == 'Log out':
        sys.exit("Log out successfully")

    luggage_description = input("Please enter a luggage description. Enter 'Log out' if you want to quit: ")



    if luggage_description == 'Log out':
        sys.exit("Log out successfully")

    sourcelo = input("Please enter a source location. Enter 'Log out' if you want to quit: ")

    if sourcelo == 'Log out':
        sys.exit("Log out successfully")

    else:
        return_sourcelo = check_location(sourcelo)


    destinationlo = input("Please enter a destination location. Enter 'Log out' if you want to quit: ")

    if destinationlo == 'Log out':
        sys.exit("Log out successfully")

    else:
        returndestinationlo = check_location(destinationlo)

       # enroute = input("Please enter an enroute location by one space (optional): ")

    # do not know how to deal with enroute locode and

    #if not enroute:
        #enroute1 = enroute[0] + enroute[1] + enroute[2]
        #return_sourcelo = check_location(enroute1)
        #enroute2 = enroute[4] + enroute[5] + enroute[6]
        #returndestinationlo = check_location(enroute2)

    cursor.execute("insert into rides values ('%%d','%%d', '%%s', '%%d', '%%s', '%%s', '%%s', '%%s','%%d')" % (None, price, date, noseats,return_sourcelo, returndestinationlo,email, entered1))
