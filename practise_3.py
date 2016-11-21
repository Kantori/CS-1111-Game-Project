# Write a function that takes two lists of integers,
# sum the two lists together and return the resulting list.
# For example if the two lists are [1,2,3] and [4,5,6,7],
# your code would return [5, 7, 9, 7]
#
# Do not use any built-in functions
# except len(), remove(), and append()
#

def sumLists(x,y):
    result = x
    not_result = y
    if len(x) < len(y):
        result = y
        not_result = x
    for i in range(len(not_result)):
        result[i] += not_result[i]










    return result


print(sumLists([], []))      # expected []
print(sumLists([1], [2]))    # expected [3]
print(sumLists([], [1]))     # expected [1]
print(sumLists([1], []))     # expected [1]
print(sumLists([2,7,3,1,9,5,5,4,6,8], [3,2,1]))     # expected [5, 9, 4, 1, 9, 5, 5, 4, 6, 8]


