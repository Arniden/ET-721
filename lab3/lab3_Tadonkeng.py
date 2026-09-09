"""
lab 3: Introduction to Python Basics
Arnaud Tadonkeng
Sep 9, 2026
"""
print(" ----- Example 1: Strings -----")
name = "Michael Jackson"
print(name[::2])
print(name[3:10:2])

print(" ----- Example 2: String Methods -----")
name1 = name.upper()
name2 = name.lower()
name3 = name.replace('Michael', 'Janet')
indexname = name.find('Jack')
print(f'Name in uppercase {name1}')
print(f'Name in lowercase {name2}')
print(f'Index for Jack = {indexname}')
print(f'split name = {name.split()}')

print(" ----- Example 3: Regular Expression -----")
#import the module for regular expression, re
import re

s1 = "Micheal Jackson is the best"
# define the pattern to search for
pattern = r"Jackson"
# use the search() function to search for the patern in the string 
result = re.search(pattern, s1)
#print result
print(f"The pattern result is {result}")
if result:
    print("Match found!")
else:
    print("Match not found.")

pattern = r"\d\d\d\d\d" # matches any five consecutive digits
zipcode = "My zipcode is 12345"
match = re.search(pattern, zipcode)
if match:
    print("Zip code found:", match.group())
else:
    print("Zip code NOT found")

print(" ----- Example 4: tuples -----")
#create a tuple
tuple1 = ("disco", 10, 1.2)
print(type(tuple1))
print(f"Second element = {tuple1[1]}")
print(f"Last element = {tuple1[-1]}")
print(f"There are {len(tuple1)} elements in the tuple")

rating =(10,3,4,9,7)
print(f"Sorted tuple = {sorted(rating)}")

#nested tuple
nestedtuple = (1,2, ("pop", "rock"), (3,4), ("disco", (8,9)))
print(f'original tuple = {nestedtuple}')
print(f"nested tuple = {nestedtuple[2]}")
print(f"nested subtuple = {nestedtuple[3][1]}")
print(f"nested sub-subtuple = {nestedtuple[4][1][0]}")

print(" ----- Example 5: dictionary -----")
#create a dictionary
release_year_dict = {
    "Thriller": 1982,
    "Back in Black": 1980,
    "The Dark Side of the Moon": 1973,
    "The Bodyguard": 1992,
    "Rumours": 1977
}

#get the value of a key
print(f"Year of the bodyguard = {release_year_dict['The Bodyguard']}")
print(f"All keys = {release_year_dict.keys()}")

#add or update an entry in a dictionary
release_year_dict["Graduation"] = 2007

#print all the keys
print(f"All keys = {release_year_dict.keys()}")

print(" \n ----- Example 6: list -----")

# create set
set1 = {"pop", "rock", "soul", "hard rock", "rock", "R&B", "disco", "rock"}
print(set1)
check1 = "AC/DC" in set1
print(f"Is AC/DC in genres? {check1}")
#add an element
set1.add("AC/DC")
check1 = "AC/DC" in set1
print(f"Is AC/DC in genres? {check1}")

album1 = {"Thriller", "Back in Black", "Rumours"}
album2 = {"Rumours", "The Dark Side of the Moon", "Back in Black"}
#intersions, &, returns the elements that are in both sets
print(album1 & album2)
# union, |, returns the element of both sets
print(album1 | album2)
# difference, ^ returns the elements that are in set but not in the other set
print(album1 ^ album2)
