# Erick Anderson, #001037222
# the slowest function in this program is O(N^3) which makes the entire program O(N^3)
import sys
from datetime import datetime, timedelta
from HashTable import PackageHashTable
from Truck import Truck
from package import Package
from map import Hub, Map


# function to parse all package data from the csv file.
# provided excel file is saved in CSV form to ease data parsing
def parse_package_data(filename):
    all_deliveries = PackageHashTable()
    iterable_packages = []

    # open file in read mode
    f = open(filename, "r")

    # read each line into a list
    all_packages = f.readlines()

    # take each line, and split it into the attributes.
    for line in all_packages:
        line = line.strip('\n')
        package_data = line.split(',')

        # assign each data to a variable, then use those variables to create a new package object
        # strip the weird characters that show up on the 1st index
        package_id = int(package_data[0].strip('ï»¿'))
        address = package_data[1]
        city = package_data[2]
        state = package_data[3]
        zipcode = package_data[4]
        delivery_time = package_data[5]
        mass = package_data[6]
        truck = package_data[7]
        delayed = package_data[8]
        pair_with = package_data[9].split()
        pair_with = [int(i) for i in pair_with]

        new_package = Package(package_id, address, city, state, zipcode, delivery_time, mass, truck, delayed,
                              pair_with)

        # adds the package to the hash table
        all_deliveries.insert(new_package)
        iterable_packages.append(new_package)

    return all_deliveries, iterable_packages


# function to parse all map data from the map
# provided excel spreadsheet converted to csv
def parse_map_data(filename):
    master_map = Map()

    # open the file to parse
    f = open(filename, "r")

    # reads the first line, which is every address, and assigns to a list
    all_addresses = f.readline().split(',')
    # strips that weird character off the first index
    all_addresses[0] = all_addresses[0].strip('ï»¿')

    # reads the rest of the file
    all_vertices = f.readlines()
    all_weights = []
    all_hubs = []

    # creates all edges and builds adjacency list
    for line in all_vertices:
        address = line.split(',')

        # creates a list of all possible addresses from the first index of each edge weight list
        new_hub = Hub(address[0])
        all_hubs.append(new_hub)
        master_map.add_hub(new_hub)

        # converts values from string to float
        for i in range(1, len(address)):
            address[i] = address[i].strip('\n')
            address[i] = float(address[i])

        all_weights.append(address)

    # builds the adjacency list
    for weight in all_weights:
        hub_a = Hub(weight[0])
        for i in range(1, len(weight)):
            hub_b = all_hubs[i - 1]
            distance = weight[i]
            master_map.add_undirected_edge(hub_a, hub_b, distance)

    start_hub = all_hubs[0]

    return master_map, all_hubs, start_hub


def search_packages(search_option, condition):
    # retrieve all packages from the hash table, and evaluates for condition
    # if the function finds no match, the found variable remains false and triggers the not found message

    found = False
    for bucket in all_packages.packages:
        for package in bucket:
            if search_option is 1:
                if package.package_id is condition:
                    package.print_all()
                    found = True

            if search_option is 2:
                if condition.lower() in package.address.lower():
                    package.print_all()
                    found = True

            if search_option is 3:
                if condition.lower() in package.city.lower():
                    package.print_all()
                    found = True

            if search_option is 4:
                if condition in package.zip:
                    package.print_all()
                    found = True

            if search_option is 5:
                if condition in package.mass:
                    package.print_all()
                    found = True

            if search_option is 6:
                if condition.lower() in package.deadline.lower():
                    package.print_all()
                    found = True

            if search_option is 7:
                if condition.lower() in package.status.lower():
                    package.print_all()
                    found = True

    if found is False:
        print('Package not found')


# this is the entry point for the user interface, and this function calls all other related menu functions
def main_menu():

    print('')
    print('Current Time: ', stop_time)
    print('')
    print('MENU')
    print('1. Search for Package')
    print('2. Show All Packages')
    print('3. Insert New Package')
    print('4. Edit Existing Package')
    print('0. Exit')

    menu_input = input()

    while menu_input == '':
        print('')
        print('Current Time: ', stop_time)
        print('')
        print('MENU')
        print('1. Search for Package')
        print('2. Show All Packages')
        print('3. Insert New Package')
        print('4. Edit Existing Package')
        print('0. Exit')

        menu_input = input()
    menu_input = int(menu_input)

    if menu_input is 1:
        menu_search_package()

    if menu_input is 2:
        all_packages.print_all()
        main_menu()

    if menu_input is 3:
        menu_new_package()

    if menu_input is 4:
        menu_edit_package()

    print('Thank You! Goodbye')
    sys.exit(0)


def menu_search_package():
    menu_input = None
    while menu_input is not 8:

        print('')
        print('Search By ')
        print('1. Package ID')
        print('2. Delivery Address')
        print('3. Delivery City')
        print('4. Delivery Zip Code')
        print('5. Weight')
        print('6. Deadline')
        print('7. Delivery Status')
        print('8. Return to Main Menu')
        menu_input = input()

        while menu_input == '':
            print('')
            print('Search By ')
            print('1. Package ID')
            print('2. Delivery Address')
            print('3. Delivery City')
            print('4. Delivery Zip Code')
            print('5. Weight')
            print('6. Deadline')
            print('7. Delivery Status')
            print('8. Return to Main Menu')
            menu_input = input()

        menu_input = int(menu_input)

        if menu_input is 1:
            print('Enter Package ID:')
            condition = input()
            while condition == '':
                print('Enter Package ID:')
                condition = input()
            condition = int(condition)
            search_packages(menu_input, condition)

        elif menu_input is 2:
            print('Enter Address:')
            condition = str(input())
            while condition == '':
                print('Enter Address:')
                condition = str(input())
            search_packages(menu_input, condition)

        elif menu_input is 3:
            print('Enter City:')
            condition = str(input())
            while condition == '':
                print('Enter City:')
                condition = str(input())
            search_packages(menu_input, condition)

        elif menu_input is 4:
            print('Enter Zip Code:')
            condition = str(input())
            while condition == '':
                print('Enter Zip Code:')
                condition = str(input())
            search_packages(menu_input, condition)

        elif menu_input is 5:
            print('Enter Weight:')
            condition = str(input())
            while condition == '':
                print('Enter Weight:')
                condition = str(input())
            search_packages(menu_input, condition)

        elif menu_input is 6:
            print('Enter Deadline (9:00 AM, 10:30 AM, EOD):')
            condition = str(input())
            while condition == '':
                print('Enter Deadline (9:00 AM, 10:30 AM, EOD):')
                condition = str(input())
            search_packages(menu_input, condition)

        elif menu_input is 7:
            print('Enter Status (On Truck 1, On Truck 2, On Truck 3, Delivered:')
            condition = str(input())
            while condition == '':
                print('Enter Status (On Truck 1, On Truck 2, On Truck 3, Delivered:')
                condition = str(input())
            search_packages(menu_input, condition)

        elif menu_input is 8:
            print('Returning to Menu')
            main_menu()

        else:
            print('Invalid Entry')


def menu_new_package():

    print('Enter Address:')
    address = str(input())
    # checks that the entry is not blank
    while address == '':
        print('Invalid entry. Please enter an address:')
        address = str(input())
    print('Enter City:')
    city = str(input())
    while city == '':
        print('Invalid entry. Please enter a city:')
        city = str(input())
    print('Enter State:')
    state = str(input())
    while state == '':
        print('Please Enter a State:')
        state = str(input())
    print('Enter 5 digit Zip Code:')
    zipcode = str(input())
    # confirms that the zipcode is 5 digits long
    while not len(zipcode) is 5:
        print('Invalid entry. Please enter a valid 5 digit zip code:')
        zipcode = str(input())
    print('Enter Weight:')
    mass = input()
    # confirms that mass is an integer
    while mass == '':
        print('Invalid Entry. Please enter an integer for the weight: ')
        mass = input()
    mass = int(mass)
    print('Choose Delivery Deadline: 1 - 9:00 AM  2 - 10:30 AM 3 - EOD:')
    deadline = input()
    # ensures a valid entry
    while deadline == '':
        print('Invalid entry. Choose Delivery Deadline: 1 - 9:00 AM  2 - 10:30 AM 3 - EOD:')
        deadline = input()
    deadline = int(deadline)
    while deadline not in [1, 2, 3]:
        print('Invalid entry. Choose Delivery Deadline: 1 - 9:00 AM  2 - 10:30 AM 3 - EOD:')
        deadline = int(input())
    if deadline is 1:
        deadline = '9:00 AM'
    if deadline is 2:
        deadline = '10:30 AM'
    if deadline is 3:
        deadline = 'EOD'
    print('Does the package need to be on a specific truck? 1 for YES, 2 for NO:')
    answer = input()
    while answer == '':
        print('Invalid entry. Does the package need to be on a specific truck? 1 for YES, 2 for NO:')
        answer = input()
    answer = int(answer)
    while answer not in [1, 2]:
        print('Invalid entry. Does the package need to be on a specific truck? 1 for YES, 2 for NO:')
        answer = int(input())

    if answer is 1:
        print('Enter truck number 1, 2, or 3:')
        truck = input()
        while truck == '':
            print('Please enter a number 1-3:')
            truck = input()
        truck = int(truck)
        while truck not in range(1, 4):
            print('Please enter a number 1-3:')
            truck = int(input())

    if answer is 2:
        truck = ''
    print('Is the package delayed? 1 for yes, 2 for no:')
    delayed = input()
    while delayed == '':
        print('Invalid entry. Is the package delayed? 1 for yes, 2 for no:')
        delayed = input()
    delayed = int(delayed)
    while delayed not in [1, 2]:
        print('Invalid entry. Is the package delayed? 1 for yes, 2 for no:')
        delayed = int(input())
    if delayed is 1:
        delayed = True
    if delayed is 2:
        delayed = False
    print('Must the package be paired with another package? 1 for yes, 2 for no:')
    answer = input()
    while answer == '':
        print('Invalid entry. Must the package be paired with another package? 1 for yes, 2 for no:')
        answer = input()
    answer = int(answer)
    while answer not in [1, 2]:
        print('Invalid entry. Must the package be paired with another package? 1 for yes, 2 for no:')
        answer = int(input())
    if answer is 1:
        print('Enter ID of package to be paired with:')
        paired_with = input()
        while paired_with == '':
            print('Package not found. Enter ID of package to be paired with:')
            paired_with = input()
        paired_with = int(paired_with)
        while paired_with not in range(1, all_packages.total_packages):
            print('Package not found. Enter ID of package to be paired with:')
            paired_with = int(input())
    if answer is 2:
        paired_with = ''

    # assembles the new package
    # auto-increments the package ID number
    package_id = all_packages.total_packages + 1

    new_package = Package(package_id, address, city, state, zipcode, deadline, mass, truck, delayed, paired_with)
    all_packages.insert(new_package)
    new_package.print_all()
    main_menu()


def menu_edit_package():
    menu_input = None
    print('Enter ID of package to edit. 0 to cancel: ')
    package_id = input()
    while package_id == '':
        print('Enter ID of package to edit. 0 to cancel: ')
        package_id = input()
    package_id = int(package_id)
    current_package = all_packages.search(package_id)

    current_package.print_all()

    while menu_input is not 0:

        print('Select attribute to edit. Enter 0 when finished.')
        print('1: Address')
        print('2: City')
        print('3: Zip Code')
        print('4: Weight')
        print('5: Deadline')
        print('6: Status')
        menu_input = input()

        while menu_input == '':
            print('Select attribute to edit. Enter 0 when finished.')
            print('1: Address')
            print('2: City')
            print('3: Zip Code')
            print('4: Weight')
            print('5: Deadline')
            print('6: Status')
            menu_input = input()
        menu_input = int(menu_input)

        if menu_input is 0:
            break
        if menu_input is 1:
            print('Enter New Address:')
            address = str(input())
            while address == '':
                print('Invalid entry. Please enter an address:')
                address = str(input())
            current_package.address = address
        if menu_input is 2:
            print('Enter New City:')
            city = str(input())
            while city == '':
                print('Invalid entry. Please enter a city:')
                city = str(input())
            current_package.city = city
        if menu_input is 3:
            print('Enter New Zip Code:')
            zipcode = str(input())
            while zipcode == '':
                print('Invalid entry. Please enter a Zip Code:')
                zipcode = str(input())
            current_package.zip_code = zipcode

        if menu_input is 4:
            print('Enter New Weight:')
            weight = input()
            while weight == '':
                print('Please Enter New Weight:')
                weight = input()

            current_package.mass = int(weight)

        if menu_input is 5:
            print('Select new deadline | 1 - 9:00 AM | 2 - 10:30 AM | 3 - EOD:')
            deadline = int(input())
            while deadline not in [1, 2, 3]:
                print('Invalid entry. Please select a deadline:')
                deadline = int(input())
            if deadline is 1:
                current_package.deadline = '9:00 AM'
            if deadline is 2:
                current_package.deadline = '10:30 AM'
            if deadline is 3:
                current_package.deadline = 'EOD'

        if menu_input is 6:
            print('Enter New Status:')
            status = str(input())
            while status == '':
                print('Invalid entry. Please enter a status:')
                status = str(input())
            current_package.status = status

        print('')
        current_package.print_all()
        print('')
        main_menu()


# main program
# parses the package and map data from the files
all_packages, iterable_packages = parse_package_data('WGUPSPackageFile.csv')

master_map, all_hubs, start_hub = parse_map_data('WGUPSDistanceTable .csv')

# prompts the user to input a time. The program will then simulate delivery up to the given time.
# in deploy version, the program would fetch the current time from the system.
print('WGUPS Routing App')
print('')
print('Please enter a time to inspect:')

stop_hour = ''
print('Enter Hour:')
stop_hour = str(input())

# ensures a valid hour is entered
while stop_hour == '':
    print('Enter Hour:')
    stop_hour = str(input())
stop_hour = int(stop_hour)

stop_min = ''
print('Enter Minute:')
stop_min = str(input())
while stop_min == '':
    print('Enter Minute:')
    stop_min = int(input())
stop_min = int(stop_min)
stop_time = datetime(2020, 1, 2, stop_hour, stop_min)

# runs the delivery simulation up until stop time
# first creates Truck 2, and then loads the packages that are specific to it
truck_2 = Truck(2, iterable_packages)
truck_2.load_truck_specific_packages()
# delayed packages go on truck 2, which will wait to leave until delayed packages are loaded
truck_2.load_delayed_packages()

# truck_2 passes the package list to truck_1
iterable_packages = truck_2.iterable_packages
truck_1 = Truck(1, iterable_packages)

# packages that need to be paired on the same truck will load onto truck 1
# any package with a priority deadline which is not delayed will also go on truck 1
truck_1.load_earliest_packages()
truck_1.load_paired_packages()
truck_1.load_priority_packages()
iterable_packages = truck_1.iterable_packages
truck_1.load_remaining_packages(iterable_packages)

# loads the rest of truck_2
iterable_packages = truck_1.iterable_packages
# double checks for more priority packages. There shouldn't be in this simulation, but could be in another package set
truck_2.load_priority_packages()
truck_2.load_remaining_packages(iterable_packages)

# create and load Truck 3. only packages that are to be delivered by the end of the day
# truck 1 driver will take truck 3 out when they get back
truck_3 = Truck(3, iterable_packages)
truck_3.load_remaining_packages(iterable_packages)

# all packages will have their status updated in the hash table


# deploy Truck 1 at 8:00
current_time = datetime(2020, 1, 2, 8, 0)

truck_1_finish_time = truck_1.deliver_packages(master_map, current_time, stop_time)


# advances current time to 9:05 to give time to load delayed packages. Then, deploy truck 2
time_elapsed = timedelta(seconds=(70 * 60))
current_time = current_time + time_elapsed

if stop_time >= current_time:
    truck_2.deliver_packages(master_map, current_time, stop_time)

if stop_time >= current_time:
    if truck_1.finished_route is True:
        truck_3.deliver_packages(master_map, truck_1_finish_time, stop_time)


# launches the user interface, allowing user to explore the packages at the given time
main_menu()
