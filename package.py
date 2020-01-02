# i am storing the package as a custom object data structure
# this allows easy access to each of the various attributes of the package
# and this also allows multiple references to the same package object at various points in the program

class Package:
    def __init__(self, package_id, address, city, state, zip_code, deadline, mass, truck, delayed, pair_with,
                 status='waiting for delivery'):

        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip_code
        self.deadline = deadline
        self.mass = mass
        self.truck = truck
        self.delayed = delayed
        self.pair_with = pair_with
        self.status = status

    # sets the hash value to the package id
    def __hash__(self):
        return hash(self.package_id)

    def print_all(self):
        print('Package ID:', self.package_id, '| Address:', self.address, '| City:', self.city, '| State:', self.state,
              '| Zip:', self.zip, '| Weight:', self.mass,  '| Status:', self.status)


