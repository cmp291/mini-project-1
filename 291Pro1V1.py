
def login():
    print("Login")
def register():
    print("Register")
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
    startscreen()

if __name__ == "__main__":
    main()
