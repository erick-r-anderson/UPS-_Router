# implementing a chaining hash table. will use ten buckets
# packages will be inserted as objects. key will be the package_id
# based on the chaining hash table introduced in the Zybooks text, section 7.8
# Data Structures and Algorithms by authors Roman Lysecky and Frank Vahid


class PackageHashTable:
    def __init__(self, total_buckets=10):
        self.packages = []
        # tracks the total number of packages in the hash table.
        self.total_packages = 0
        # initialize each bucket as an empty list
        for i in range(total_buckets):
            self.packages.append([])

    def insert(self, package):
        # O(N)
        # find the proper bucket, append the package to that bucket's list
        bucket = hash(package) % len(self.packages)
        bucket_list = self.packages[bucket]

        # insert item into bucket
        bucket_list.append(package)
        self.total_packages += 1

    # search for package by package_id
    def search(self, package_id):
        # O(N)
        # will find the proper bucket, then search the list
        bucket = package_id % len(self.packages)
        bucket_list = self.packages[bucket]

        for package in bucket_list:
            if package.package_id == package_id:
                # get the package's index, then use the index to return the item
                package_index = bucket_list.index(package)
                return package
        else:
            # key is not in the table
            return None

        # remove function
    def remove(self, package_id):
        # get the bucket list
        # O(N)
        bucket = package_id % len(self.packages)
        bucket_list = self.packages[bucket]

        # remove the item if it's present. won't remove if not present
        for package in bucket_list:
            if package.package_id == package_id:
                bucket_list.remove(package)
                self.total_packages -= 1

    # prints all packages in order of packageID
    def print_all(self):
        for i in range(1, self.total_packages + 1):
            self.search(i).print_all()
