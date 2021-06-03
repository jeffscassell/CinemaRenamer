# List
# mutable, easy to use, all the benefits of an array and a referenced object

# looks a lot like an array, but it's an object
nums = [25, 12, 15, 55]
print(nums, "\n")  # the second argument is appended to the end of the line (on top of the normal \n)

# items are accessed like an array
print(nums[0])

# items can also be accessed in ranges
print(nums[:2])
print(nums[2:])

# indexes can also be called, starting from the end of the list
print(nums[-1])

# python lists can contain multiple data types
variety = ["jeff", 5, 2.2]
print("variety list: " + str(variety))
print()

# the brackets aren't required -- but they are strongly encouraged due to tuples and sets existing
# lists can also contain other lists (2D lists)
combined = nums, variety
print(combined)

# lists are dynamic and items can be added or removed as needed
nums.append(66)
print(nums)
print()

# because the nums lists is referenced in the combined list, it is updated as well
print(combined)
print()

# remove items by value using remove(), or by index using pop()
nums.remove(66)
nums.pop(2)  # not specifying an index will pop the last (just like a stack)
print(nums)
print()

# items can also be added at a specific index -- re-arranging the indexes of everything else -- using insert(index,
# value)
nums.insert(0, 22)
print(nums)

# it is possible to delete a range
del nums[2:]
print(nums)

# and add a range
nums.extend([5, 6, 7])
print(nums)
print()

# a few built-in methods (functions, whatever) for processing lists
print(min(nums))
print(max(nums))
print(nums.count(5))  # counts the occurrences of the given value in the list
print(nums.index(22))  # returns the index of the given value
nums.sort()
print(nums)

########################################################################################################

# Dictionary
# key-value pairs. the keys are unique and immutable (but can be deleted), the values are not.

# uses curly braces, with colon to separate the key-value pairs
dic = {1: "jeff", 7: "kalina"}

# can access data like lists, but instead of specifying an index to access a value, the key is specified
print(dic[1])

# preferred way to access data is with the get() method, because if key does not exist no error is returned
print(dic.get(7))
print(dic.get(2, "key 2 does not exist"))
print()

# one way to set a new value is by specifying a key
dic[2] = "dad"
print(dic)

# to remove a key-value pair, use the del() method -- pop() can also be used similarly to lists
del dic[2]
print(dic)
print()

# dictionaries can be built from lists in a slightly complex series of steps
keys = ["jeff", "kalina", "dad", "jr"]
values = ["computers", "art", "relaxing", "weed"]
dic = dict(zip(keys, values))
print(dic)
print()

# key-value pairs do not have to match each other's data types, and can in fact store lists or other dictionaries
programs = {"JS": "Atom", "CS": "VS", "Python": ["PyCharm", "Sublime"], "Java": {"JSE": "NetBeans", "JEE": "Eclipse"}}
print(programs["Python"])
print(programs["Python"][1])
print(programs["Java"]["JEE"])

########################################################################################################

# Tuple
# immutable

# tuples use parenthesis instead of list's square bracket
tup = (10, 20, 30, 15, 12)

# attempting to add another value will throw an error
try:
    tup[0] = 0
except TypeError:
    print("tuples cannot be changed (they are immutable)")

########################################################################################################

# Set
# prioritizes speed over all else. there is no sequencing (the contents are stored randomly), and a value may occur
# only once. because it is unsequenced, it cannot be indexed

# sets use curly braces
s = {5, 21, 1, 0, 55, 10, 5}
print(s)

# cannot use indexing
try:
    s[0]
except TypeError:
    print("sets do not support indexing (subscripting)")

