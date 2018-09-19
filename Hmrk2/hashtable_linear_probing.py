# Please see instructions.pdf for the description of this problem.
from fixed_size_array import FixedSizeArray
from cs5112_hash import cs5112_hash1


# An implementation of a hash table that uses chaining to handle collisions.
class HashTable:
    def __init__(self, initial_size=10, load_factor=.75):
        # DO NOT EDIT THIS CONSTRUCTOR
        if (initial_size < 0) or (load_factor <= 0) or (load_factor > 1):
            raise Exception("size must be greater than zero, and load factor must be between 0 and 1")
        self.array_size = initial_size
        self.load_factor = load_factor
        self.item_count = 0
        self.array = FixedSizeArray(initial_size)

    # Inserts the `(key, value)` pair into the hash table, overwriting any value
    # previously associated with `key`.
    # Note: Neither `key` nor `value` may be None (an exception will be raised)
    def insert(self, key, value):
        if key is None or value is None:
            raise Exception

        # resizing if more than load factor
        if (self.item_count / self.array_size) > self.load_factor:
            self._resize_array()

        index = cs5112_hash1(key) % self.array_size

        # if index is not empty, it is either x or real tuple
        while self._get_array().get(index) is not None:
            # if it is x, it is removed. add it here.
            if self._get_array().get(index) == 'x':
                self._get_array().set(index, (key, value))
                self.item_count += 1
                break
            # the key is the same, just update the value
            elif self._get_array().get(index)[0] == key:
                self._get_array().set(index, (key, value))
                break
            else:
                # there is a real, other tuple, move on
                # wrap-around logic
                if self.array_size - 1 == index:
                    index = 0
                # just probe the next cell
                else:
                    index += 1

        if self.array.get(index) is None:
            self._get_array().set(index, (key, value))
            self.item_count += 1

    # Returns the value associated with `key` in the hash table, or None if no
    # such value is found.
    # Note: `key` may not be None (an exception will be raised)
    def get(self, key):
        if key is None:
            raise Exception

        index = cs5112_hash1(key) % self.array_size
        end = index

        while self._get_array().get(index) is not None:
            #check that not removed and is the key
            if self._get_array().get(index) != 'x' and self._get_array().get(index)[0] == key:
                return self._get_array().get(index)[1]

            # wrap-around logic
            if self.array_size - 1 == index:
                index = 0
            else:
                # just probe the next cell
                index += 1

            if index == end:
                return None

        if self._get_array().get(index) is None:
            return None

    # Removes the `(key, value)` pair matching the given `key` from the map, if it
    # exists. If such a pair exists in the map, the return value will be the value
    # that was removed. If no such value exists, the method will return None.
    # Note: `key` may not be None (an exception will be raised)
    def remove(self, key):
        if key is None:
            raise Exception

        index = cs5112_hash1(key) % self.array_size
        end = index

        while self._get_array().get(index) is not None:
            if self._get_array().get(index) != 'x' and self._get_array().get(index)[0] == key:
                value = self._get_array().get(index)[1]
                self._get_array().set(index, 'x')
                self.item_count -= 1
                return value

                # wrap-around logic
            if self.array_size - 1 == index:
                index = 0
            else:
                # just probe the next cell
                index += 1

            if index == end:
                return None

        return None


    # Returns the number of elements in the hash table.
    def size(self):
        return self.item_count

    # Internal helper function for resizing the hash table's array once the ratio
    # of stored mappings to array size exceeds the specified load factor.
    def _resize_array(self):
        array_size = self.array_size * 2
        oldArray = self.array
        self.array_size = array_size
        self.array = FixedSizeArray(array_size)
        self.item_count = 0
        # fixed sized array has a list of items.
        for i in oldArray.items:
            if i is not None and i != 'x':
                self.insert(i[0], i[1])

    # Internal helper function for accessing the array underlying the hash table.
    def _get_array(self):
        # DO NOT EDIT THIS METHOD
        return self.array

