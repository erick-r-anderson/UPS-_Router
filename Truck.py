from datetime import timedelta, datetime
from map import Hub


class Truck:

    def __init__(self, truck_id, input_packages):
        self.truck_id = truck_id
        self.loaded_packages = []
        self.iterable_packages = input_packages
        self.finished_route = True

        self.address_list = []
        self.priority_address_list = []

    def load_paired_packages(self):
        # this function is O(N^2)
        # iterates through packages, finds those that need to be paired, and then finds the packages to pair them with
        # all lists iterated through backwards, so that items can be safely removed in iteration
        for package in reversed(self.iterable_packages):
            # if the package has items in its pair with list
            if len(package.pair_with) is not 0:
                package.status = ' on truck ' + str(self.truck_id)
                self.loaded_packages.append(package)
                self.iterable_packages.remove(package)
                # searches for any additional packages which need to be paired with this current package
                for package_2 in reversed(self.iterable_packages):
                    if int(package_2.package_id) in package.pair_with:
                        package_2.status = ' on truck ' + str(self.truck_id)
                        self.loaded_packages.append(package_2)
                        self.iterable_packages.remove(package_2)

    def load_truck_specific_packages(self):
        # this function is O(N)
        # will search for any packages which are required to be on a specific truck
        for package in reversed(self.iterable_packages):
            if str(package.truck) == str(self.truck_id):
                package.status = 'on truck ' + str(self.truck_id)
                self.loaded_packages.append(package)
                self.iterable_packages.remove(package)

    def load_delayed_packages(self):
        # this function is O(N)
        # these packages will always go out on Truck 2, the truck which leaves later
        if self.truck_id == 2:
            for package in reversed(self.iterable_packages):
                if package.delayed:
                    package.status = ' on truck ' + str(self.truck_id)
                    self.loaded_packages.append(package)
                    self.iterable_packages.remove(package)

    def load_priority_packages(self):
        # this function is O(N)
        # loads the first truck with the packages needing to be delivered earlier
        for package in reversed(self.iterable_packages):
            if len(self.loaded_packages) > 16:
                break
            elif package.deadline != 'EOD':
                package.status = ' on truck ' + str(self.truck_id)
                self.loaded_packages.append(package)
                self.iterable_packages.remove(package)

        # at this point in the algorithm, packages which are required to be on a specific truck will be loaded
        # now, we start searching for packages which can be delivered with any already loaded
        self.load_matching_packages()

    def load_remaining_packages(self, iterable_packages):
        # this function is O(N^2)
        # final load operation, will fill truck's remaining space
        self.iterable_packages = iterable_packages
        for package in reversed(self.iterable_packages):
            # ensures there is room on the truck,a nd that the package is not a priority package
            if len(self.loaded_packages) < 16:
                package.status = ' on truck ' + str(self.truck_id)
                self.loaded_packages.append(package)
                self.iterable_packages.remove(package)
                # for each package loaded this way, will then check for a package with matching address
                for package_2 in reversed(self.iterable_packages):
                    if len(self.loaded_packages) < 16:
                        if package_2.address is package.address:
                            package_2.status = ' on truck ' + str(self.truck_id)
                            self.loaded_packages.append(package_2)
                            self.iterable_packages.remove(package_2)

    def load_matching_packages(self):
        # will load any packages whose address matches a package already loaded
        # this function is O(N^2)
        for package in reversed(self.loaded_packages):
            # checks to make sure there is still room on the truck
            if len(self.loaded_packages) < 16:
                for package_2 in reversed(self.iterable_packages):
                    if package_2.address is package.address:
                        package_2.status = ' on truck ' + str(self.truck_id)
                        self.loaded_packages.append(package_2)
                        self.iterable_packages.remove(package_2)

    def load_earliest_packages(self):
        # this function is O(N)
        # loads any package with an early deadline
        for package in reversed(self.iterable_packages):
            if package.deadline is '9:00 AM':
                package.status = ' on truck ' + str(self.truck_id)
                self.loaded_packages.append(package)
                self.iterable_packages.remove(package)

    # build the list of addresses this truck needs to visit, will be the unvisited queue for dykstra's
    def build_address_list(self):
        # O(N)
        for package in self.loaded_packages:
            if package.address not in self.priority_address_list:
                self.address_list.append(package.address)

    def build_priority_address_list(self):
        # O(N)
        for package in self.loaded_packages:
            if package.deadline != 'EOD':
                self.priority_address_list.append(package.address)

    def deliver_priority_packages(self, g, time, stop):
        # based on the implementation of Dijkstra's algorithm as introduced in the Zybooks text, section 6.12
        # Data Structures and Algorithms by authors Roman Lysecky and Frank Vahid
        # O(N^2) due to three nested loops
        speed = 18.0
        current_time = time
        stop_time = stop
        total_miles = 0

        unvisited_queue = []
        start_hub = Hub('HUB')

        # builds unvisited queue by matching each package address with the associated hub on the master map
        for current_hub in g.adjacency_list:
            for address in self.priority_address_list:
                if address == current_hub.address:
                    unvisited_queue.append(current_hub)

        start_hub.distance = 0

        # initializes the previous hub to be the start hub. this will change with each iteration
        previous_hub = start_hub

        # checks for the package with the earliest deadline, visits that hub first no matter what
        for package in self.loaded_packages:
            if package.deadline == '9:00 AM':
                for hub in unvisited_queue:
                    if hub.address == package.address:
                        current_hub = hub
                        unvisited_queue.remove(hub)
                        # calculate the minutes traveled since the last stop
                        distance_traveled = g.edge_weights[(previous_hub, current_hub)]
                        total_miles += distance_traveled
                        minutes_traveled = ((1.0 / speed) * 60.0) * distance_traveled
                        # create time delta, converting minutes to seconds
                        time_elapsed = timedelta(seconds=(minutes_traveled * 60))
                        current_time = current_time + time_elapsed

                        # delivers associated packages to each address when visited

                        for package in reversed(self.loaded_packages):
                            if package.address == current_hub.address:
                                # deliver package
                                package.status = "delivered to " + current_hub.address

                                # removes the loaded package from the truck's loaded list
                                self.loaded_packages.remove(package)
                                package.status = ' delivered to ' + current_hub.address + ' by Truck ' + str(self.truck_id) \
                                                 + ' at ' + str(current_time) + '. Deadline: ' + package.deadline

                        previous_hub = current_hub

        while len(unvisited_queue) > 0:

            # find hub with minimum distance from the start, and visit it
            smallest_index = 0
            for i in range(len(unvisited_queue)):
                if unvisited_queue[i].distance < unvisited_queue[smallest_index].distance:
                    smallest_index = i
            current_hub = unvisited_queue.pop(smallest_index)

            # calculate the minutes traveled since the last stop
            distance_traveled = g.edge_weights[(previous_hub, current_hub)]
            minutes_traveled = ((1.0 / speed) * 60.0) * distance_traveled
            # create time delta, converting minutes to seconds
            time_elapsed = timedelta(seconds=(minutes_traveled * 60))
            current_time = current_time + time_elapsed

            # cuts off delivery of packages at the chosen stop time
            if stop_time <= current_time:
                self.finished_route = False
                break
            # delivers associated packages to each address when visited
            for package in reversed(self.loaded_packages):
                if package.address == current_hub.address:
                    # deliver package
                    package.status = "delivered to " + current_hub.address

                    # removes the loaded package from the truck's loaded list
                    self.loaded_packages.remove(package)
                    package.status = ' delivered to ' + current_hub.address + ' by Truck ' + str(self.truck_id) + \
                                     ' at ' + str(current_time) + '. Deadline: ' + package.deadline

            # at the end of the loop, sets the previous hub to be the current hub
            previous_hub = current_hub

        return current_time, total_miles

    def deliver_packages(self, g, time, stop):
        # based on the implementation of Dijkstra's algorithm as introduced in the Zybooks text, section 6.12
        # Data Structures and Algorithms by authors Roman Lysecky and Frank Vahid
        # O(N^2) due to two nested loops
        start_time = time
        stop_time = stop

        package_9_update_time = datetime(2020, 1, 2, 10, 20)

        # delivers all priority packages first
        self.build_priority_address_list()
        current_time, total_miles = self.deliver_priority_packages(g, start_time, stop_time)

        self.build_address_list()
        # constant speed of 18 miles per hour
        speed = 18.0

        unvisited_queue = []
        start_hub = Hub('HUB')

        # builds unvisited queue by matching each package address with the associated hub on the master map
        for current_hub in g.adjacency_list:
            for address in self.address_list:
                if address == current_hub.address:
                    unvisited_queue.append(current_hub)

        start_hub.distance = 0  # visits each hub, removing it when visited.

        # initializes the previous hub to be the start hub. this will change with each iteration
        previous_hub = start_hub

        while len(unvisited_queue) > 0:
            if stop_time <= current_time:
                self.finished_route = False
                break
            # find hub with minimum distance from the start, and visit it
            smallest_index = 0
            for i in range(len(unvisited_queue)):
                if unvisited_queue[i].distance < unvisited_queue[smallest_index].distance:
                    smallest_index = i
            current_hub = unvisited_queue.pop(smallest_index)

            # calculate the minutes traveled since the last stop
            distance_traveled = g.edge_weights[(previous_hub, current_hub)]
            total_miles += distance_traveled
            minutes_traveled = ((1.0 / speed) * 60.0) * distance_traveled
            # create time delta, converting minutes to seconds
            time_elapsed = timedelta(seconds=(minutes_traveled * 60))
            current_time = current_time + time_elapsed

            # stops delivery simluation at the appropriate time
            if stop_time <= current_time:
                self.finished_route = False
                break
            # delivers associated packages to each address when visited
            for package in self.loaded_packages:
                # will reject package 9 for delivery until the address is corrected at 10:20
                if package.package_id == 9:
                    address_correction_time = datetime(2020, 1, 2, 10, 20)
                    if current_time < address_correction_time:
                        package.status = 'delivery rejected, incorrect address'
                        unvisited_queue.append(current_hub)
                        package = next in self.loaded_packages
                    else:
                        package.address = '410 S State St'
                        # ensures that if that address was already visited, the truck returns to it
                        for hub in g.adjacency_list:
                            if package.address == hub.address:
                                unvisited_queue.append(hub)

                if package.address == current_hub.address:
                    # removes the loaded package from the truck's loaded list
                    self.loaded_packages.remove(package)
                    package.status = ' delivered to ' + current_hub.address + ' by Truck ' + str(
                        self.truck_id) + ' at ' + str(current_time) + ' Deadline: ' + package.deadline

            # at the end of the loop, sets the previous hub to be the current hub
            previous_hub = current_hub

        # at the end of route, calculate the time to return to the hub, and then log that time
        distance_traveled = g.edge_weights[(previous_hub, start_hub)]
        minutes_traveled = ((1.0 / speed) * 60.0) * distance_traveled
        # create time delta, converting minutes to seconds
        time_elapsed = timedelta(seconds=(minutes_traveled * 60))
        current_time = current_time + time_elapsed

        if self.finished_route is True:
            print('Truck ', self.truck_id, ' returned to hub at ', current_time, ' and traveled ', total_miles, 'miles')
        else:
            print('Truck ', self.truck_id, 'still out for delivery')
        return current_time

    def print_packages(self):
        # used for debugging purposes
        # O(N)

        if len(self.loaded_packages) == 0:
            print('all packages delivered')
        else:
            for package in self.loaded_packages:
                print(package.package_id, package.deadline, package.status)
