import os
import random
import json
from time import sleep

movies = {}
user_selection = {}

filename_user_selection = r'.\user_selection.json'
if os.path.exists(r'.\user_selection.json'):
    with open(filename_user_selection, 'r') as f:
        user_selection = json.load(f)
else:
    user_selection = {}

filename = r'.\user_pass.json'
if os.path.exists(r'.\user_pass.json'):
    with open(filename, 'r') as f:
        user_pass = json.load(f)
else:
    user_pass = {}


def ShowTimes():
    i = input("Enter a show time or s to stop: ")
    t = []
    while i != 's':
        t.append(i)
        i = input("Enter a show time or s to stop: ")
    return t


def removeFromName(name):
    if ("(" or ")" or "[" or "]") in name:
        n1 = name[name.index("("):name.index(")") + 1]
        n2 = name[name.index("["):n16ame.index("]") + 1]
        name = name.replace(n1, "")
        name = name.replace(n2, "")
    return name


def snacks(username):
    total = 0
    popcorn = 0
    nachos = 0
    dips = 0
    cookies = 0
    ice_cream = 0
    gummy_bears = 0
    soft_drinks = 0
    water = 0
    order = input("Do you want a snack? (yes or no): ").lower()
    finish = 'no'
    if order == 'no':
        print("Okay thank you!!")
    while order != 'no':
        print(
            "1-popcorn 110000L.L\n2-nachos 150000L.L\n3-dips 50000L.L\n4-cookies 90000L.L\n5-ice cream70000\n6-gummy bears 50000L.L\n7-soft drinks 25000L.L\n8-water 10000L.L")
        snack = int(input("Which snack do you want? "))
        if snack == 1:
            popcorn += 1
            price = 110000
        if snack == 2:
            nachos += 1
            price = 150000
        if snack == 3:
            dips += 1
            price = 50000
        if snack == 4:
            cookies += 1
            price = 90000
        if snack == 5:
            ice_cream += 1
            price = 70000
        if snack == 6:
            gummy_bears += 1
            price = 50000
        if snack == 7:
            soft_drinks += 1
            price = 25000
        if snack == 8:
            water += 1
            price = 10000
        total = total + price
        order = input("Do you want another snack? (yes or no): ").lower()

    user_selection[username][1] += total
    with open(r".\user_selection.json", "w+") as outfile:
        json.dump(user_selection, outfile)
    return [popcorn, nachos, dips, cookies, ice_cream, gummy_bears, soft_drinks, water], total


def printMovies():
    index = 0
    for key, value in movies.items():
        index += 1
        print(index, "- Name:", removeFromName(key))
        print("\tDuration:", value[0])

        t = ""
        for i in range(len(value[4])):
            t += value[4][i]
            if i != len(value[4]) - 1:
                t += ", "

        print("\tAvailable show times:", t)
        print("\tPrice per ticket: ", value[1], " LBP", sep="")


def selectSeats(username, name):
    total_price = 0

    def printSeats():
        count = 0
        for i in movies[name][2]:
            print(i, end="\t")
            count += 1
            if count == 10:
                print()
                count = 0

    printSeats()

    number_of_seats = 0

    seat = int(input("Select your seats: "))
    while seat != -1:
        if all(p == 'X' or p == 'S' for p in movies[name][2]):
            print("All seats are full right now.")
            break
        elif movies[name][2][seat - 1] == 'X':
            seat = int(input("Seat is unavailable. Choose another: "))
        else:
            movies[name][2][seat - 1] = 'S'
            total_price += movies[name][1]
            number_of_seats += 1
            printSeats()
            seat = int(input("Select another seat or enter '-1' to stop: "))

    movies[name][2] = ['X' if item == 'S' else item for item in movies[name][2]]

    user_selection[username][0] += removeFromName(name) + "\n\t\t\t    "
    user_selection[username][1] += total_price
    with open(r".\user_selection.json", "w+") as outfile:
        json.dump(user_selection, outfile)

    return number_of_seats, total_price


def admin_menu():
    print("(1) Add Movie")
    print("(2) Edit Movie")
    print("(3) Remove Movie")
    print("(4) View Movies")
    print("(5) Sign Out")

    def setPriceAndSeats(index):
        price = int(input("Price of the ticket (LBP): "))
        movies[index][1] = price
        seats_list = []
        for i in range(1, 101):
            if random.randrange(0, 3) == 0:
                seats_list.append('X')
            else:
                seats_list.append(i)
        movies[index][2] = seats_list

    menu_input = int(input())
    if menu_input == 1:
        path = input("Enter path to read movies or enter '1' to manually add a movie: ")

        if path == '1':
            name = input("Name of the movie: ")
            duration = input("Duration of the movie (h:m:s format): ")
            time = ShowTimes()
            movies[name] = [duration, "", "", False, time]
            setPriceAndSeats(name)
            print("Movie added successfully, returning to menu.")
            admin_menu()

        else:
            movies_list = []
            print("Reading available movies...")
            movie_list = os.listdir(path)

            count = 0
            for name in movie_list:
                movie_path = path + "\\" + name
                for file in os.listdir(movie_path):
                    if file.endswith(".mp4") or file.endswith(".avi") or file.endswith(".mkv"):
                        count += 1
                        movies_list.append(name)
                        print(count, " - ", removeFromName(name), sep="")

            while True:
                index = int(input("Enter the index of the movie you would like to add: "))
                if index <= len(movies_list):
                    print("Movie picked:", removeFromName(movies_list[index - 1]))
                    duration = input("Enter the duration of the movie (h:m:s format): ")
                    time = ShowTimes()
                    movies[movies_list[index - 1]] = [duration, "", "", path + "\\" + movies_list[index - 1], time]
                    setPriceAndSeats(movies_list[index - 1])
                    print("Movie added successfully, returning to menu.")
                    admin_menu()
                else:
                    print("Index number out of bounds, try again.")

    elif menu_input == 2:
        if len(movies) == 0:
            print("No movies have been added yet.")
        else:
            while True:
                printMovies()
                movies_list = list(movies)
                index = int(input("Enter the index of the movie you would like to edit: "))
                index = index - 1
                if movies_list[index] not in movies:
                    print("The movie you entered is not in the movies list. Try again.")
                else:
                    selection = input("(1) Edit Name\n(2) Edit Duration\n(3) Edit Show Times\n(4) Edit Price\n")
                    if selection == '1':
                        movies[input("New Name: ")] = movies.pop(movies_list[index])
                    elif selection == '2':
                        movies[movies_list[index]][0] = input("New Duration (h:m:s format): ")
                    elif selection == '3':
                        movies[movies_list[index]][4] = ShowTimes()
                    elif selection == '4':
                        movies[movies_list[index]][1] = int(input("New Price (LBP): "))
                    print("Movie edited, returning to menu.")
                    admin_menu()
        admin_menu()
    elif menu_input == 3:
        if len(movies) == 0:
            print("No movies have been added yet.")
        else:
            while True:
                printMovies()
                movies_list = list(movies)
                index = int(input("Enter the index of the movie you would like to remove: "))
                index = index - 1
                if movies_list[index] not in movies:
                    print("The movie you entered is not in the movies list. Try again.")
                else:
                    del movies[movies_list[index]]
                    print("Movie deleted, returning to menu.")
                    admin_menu()
        admin_menu()
    elif menu_input == 4:
        if len(movies) == 0:
            print("No movies have been added yet.")
        else:
            printMovies()
        admin_menu()
    elif menu_input == 5:
        print("Signing out...")
        main()


def user_menu(username):
    print("(1) Book a ticket")
    print("(2) View information")
    print("(3) Sign Out")

    menu_input = int(input())
    if menu_input == 1:
        if len(movies) == 0:
            print("Sorry, there are no movies showing now.")
            user_menu(username)
        printMovies()
        index = int(input("Pick a movie by entering its index: "))
        if all(p == 'X' for p in movies[[key for key in movies.keys()][index - 1]][2]):
            print("Sorry, all seats are full for this movie.")
            user_menu(username)
        print("Movie picked:", removeFromName([key for key in movies.keys()][index - 1]))

        print("Available show times: ")
        t_index = 0
        for i in movies[[key for key in movies.keys()][index - 1]][4]:
            t_index = t_index + 1
            print(t_index, "-", i)
        selected_time = int(input("Select a show time by entering its index: "))
        showtime = movies[[key for key in movies.keys()][index - 1]][4][selected_time - 1]

        number_of_seats, seats_price = selectSeats(username, [key for key in movies.keys()][index - 1])
        movie_name = [key for key in movies.keys()][index - 1]
        selected_snacks, snacks_price = snacks(username)

        print("\n\nMOVIE:", removeFromName(movie_name))
        print("NUMBER OF SEATS:", number_of_seats)
        if all(p != 0 for p in selected_snacks):
            print("SNACKS:")
            if selected_snacks[0] != 0:
                print("\tPopcorn:", selected_snacks[0])
            if selected_snacks[1] != 0:
                print("\tNachos:", selected_snacks[1])
            if selected_snacks[2] != 0:
                print("\tDips:", selected_snacks[2])
            if selected_snacks[3] != 0:
                print("\tCookies:", selected_snacks[3])
            if selected_snacks[4] != 0:
                print("\tIce Cream:", selected_snacks[4])
            if selected_snacks[5] != 0:
                print("\tGummy Bears:", selected_snacks[5])
            if selected_snacks[6] != 0:
                print("\tSoft Drinks:", selected_snacks[6])
            if selected_snacks[7] != 0:
                print("\tWater:", selected_snacks[7])
        print("TIME:", showtime)
        print("TOTAL PRICE:", seats_price + snacks_price, " LBP")
        print("\nEnjoy your movie!")

        if movies[movie_name][3]:
            for i in range(5, 0, -1):
                if i == 1:
                    print("Movie will start in ", i, " second.")
                else:
                    print("Movie will start in ", i, " seconds.")
                sleep(1)
            for file in os.listdir(movies[movie_name][3]):
                if file.endswith(".mp4") or file.endswith(".avi") or file.endswith(".mkv"):
                    os.startfile(movies[movie_name][3] + "/" + file)

        print()
        user_menu(username)
    elif menu_input == 2:
        print("User:", username)
        print("Movies watched:", removeFromName(user_selection[username][0]))
        print("Total price spent: ", user_selection[username][1], " LBP", sep="")
        print()
        user_menu(username)
    elif menu_input == 3:
        print("Signing out...")
        main()


def main():
    print("Welcome to PythonCinema!")
    print("Please choose an option:")
    print("(1) Log in")
    print("(2) Sign up")

    menu_input = int(input())
    if menu_input == 1:
        while True:

            username = input("Username: ")
            while username != '-1':
                password = input("Password: ")

                if username == "admin" and password == "admin":
                    print("Logged in as Admin.")
                    admin_menu()
                elif user_pass.get(username) == password:  # user_pass[username] == password:
                    print("Log in successful!")
                    user_menu(username)
                else:
                    print("Wrong username or password. Try again or type '-1' to go back to the menu.")
                    username = input("Username: ")
                    if username == '-1':
                        main()

    elif menu_input == 2:
        username = input("Enter a username: ")
        while username in user_pass.keys():
            print("This username has already been taken, try another.")
            username = input("Username: ")
        password = input("Enter a password: ")
        password_repeated = input("Re-enter password: ")
        while password != password_repeated:
            print("Passwords do not match, try again.")
            password = input("Enter a password: ")
            password_repeated = input("Re-enter password: ")
        user_pass[username] = password
        print("Sign up successful!")
        user_selection[username] = ["", 0]
    with open(r".\user_pass.json", "w+") as outfile:
        json.dump(user_pass, outfile)
    with open(r".\user_selection.json", "w+") as outfile:
        json.dump(user_selection, outfile)
    user_menu(username)


main()
