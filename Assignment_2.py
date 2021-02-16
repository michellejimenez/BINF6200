import re

"""
Problem Set 5.2

Find the match objects for the specified regex

"""

# Define sets to be tested as variables
number1 = "-255.34" 
number2 = "155"
number3 = "1.9d-10"
number4 = "1,340.00"
number5 = "720mL"
number6 = "720L"

# Call the regex function
result1 = re.search(r"([\d\.,-e]+)", number1)
resulta = re.search(r"([\.,-k\d]+)", number3)
resultb = re.search(r"([\d\.,-e]+)", number6)
result2 = re.search(r"([\d\.,-e]+)", number2)
result3 = re.search(r"([\d\.,-e]+)", number3)
result4 = re.search(r"([\d\.,-e]+)", number4)
result5 = re.search(r"([\d\.,-e]+)", number5)

# Print output of the matches
print(result1)  # <re.Match object; span=(0, 7), match='-255.34'>
print(resulta)
print(result2)  # <re.Match object; span=(0, 3), match='155'>
print(result3)  # <re.Match object; span=(0, 7), match='1.9e-10'>
print(result4)  # <re.Match object; span=(0, 8), match='1,340.00'>
print(result5)  # <re.Match object; span=(0, 3), match='720'>
# here 'mL' was not matched because re.search stops at the first location where the regex produces a match
# 'm' will not match (ASCII index 109; out of the specified range)
# therefore re.search stopped at '720' instead of also matching 'L' (ASCII index 76, which is in range from index 44 to index 101)
# "720L" would have matched all the characters


# Explanation
# re.search scans through string looking for the first location where the regular expression pattern produces a match, and return a corresponding match object
# r"([\d\.,-e]+
# [] indicates a set of characters
# \d will match a decimal digit [0-9]
# \. escaped period will match a literal period because '\' inhibits the "specialness" of a character
# ,-e matches a single character in the range between ',' (index 44) and 'e; (index 101) (case sensitive) in ASCII code
# + matches the preceding element one or more times
