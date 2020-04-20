Additional libraries used:

operator - used in search_by_price function line 282. 
Used to arrange dictionary according to lowest value. 
Output will be a list of tuple pairs.

math - for sqrt function in location-based search

nsmallest from heapq library - used in search_nearest_canteen function line 319
Creates a list of the k smallest values from a current list.

e.g.
#user wants the first 3 smallest values from list L1
k = 3 
L1 = [1,2,3,4,5,6]

print(nsmallest(k,L1)) will give the output [1,2,3].