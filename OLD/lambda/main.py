# Online Python compiler (interpreter) to run Python online.
# Write Python 3 code in this online editor and run it.
print("Hello world")
import yaml

users = {
    "users": [
        {
            "name": "Lonny", "age": 25, "city": "Lyon"
        },
        {
            "name": "Lonny", "age": 23, "city": "Bron"
        },
        {
            "name": "Lonny", "age": 13, "city": "Paris"
        },
        {
            "name": "Lonny", "age": 203, "city": "Lyon"
        },
    ]
}
def my_function():
  return "12"


# myvar = 12
# myvar = 13
# myList = [{'a': 'A'}, {'b': 'B'}, {'c': 'C', 'cc': 'CC'}]
# result = [dict(item, password=my_function()) for item in users["users"]]
# print(result)
# print(myList)

yaml_string = """
---
users:
- "key": "user[0].name"
  "value": "john"
- "key": "user[0].age"
  "value": "23"
- "key": "user[0].city"
  "value": "barcelona"
- "key": "user[0].password"
  "value": "5]L+J7rA*<7+:PO6"
- "key": "user[1].name"
  "value": "bob"
- "key": "user[1].age"
  "value": "29"
- "key": "user[1].city"
  "value": "london"
- "key": "user[1].password"
  "value": "P=x&385YGMI0?!Is"
"""

python_object = yaml.load(yaml_string, Loader=yaml.SafeLoader)

print(python_object)


import re
print("Hello world")
people = {'users': [{'key': 'user[0].name', 'value': 'john'}, {'key': 'user[0].age', 'value': '23'}, {'key': 'user[0].city', 'value': 'barcelona'}, {'key': 'user[0].password', 'value': '5]L+J7rA*<7+:PO6'},{'key': 'user[1].name', 'value': 'john'}, {'key': 'user[1].age', 'value': '23'}, {'key': 'user[1].city', 'value': 'barcelona'}, {'key': 'user[0].password', 'value': '5]L+J7rA*<7+:PO6'}, {'key': 'user[1].name', 'value': 'bob'}, {'key': 'user[1].age', 'value': '29'}, {'key': 'user[1].city', 'value': 'london'}, {'key': 'user[1].password', 'value': 'P=x&385YGMI0?!Is'}]}

# Find all cities with their corresponding users
print(list(filter(lambda person: re.match("^user\[[0-9]+\]\.city$", person['key']), people["users"])))
# --> Result: [{'key': 'user[0].city', 'value': 'barcelona'}, {'key': 'user[1].city', 'value': 'barcelona'}, {'key': 'user[2].city', 'value': 'london'}]
# Now for all do 
# Find all field except the city for the current user 
print(list(filter(lambda person: re.match("^user\[0]\.(?!city).+", person['key']), people["users"])))
# --> Result: [{'key': 'user[0].name', 'value': 'john'}, {'key': 'user[0].age', 'value': '23'}, {'key': 'user[0].password', 'value': '5]L+J7rA*<7+:PO6'}]

# Sort list of dictionaries by key
test_dict2 = {
'paris' : [
    { 'roll' : 24, 'marks' : 12},
    { 'roll' : 24, 'marks' : 11},
    { 'roll' : 24, 'marks' : 19},
    { 'roll' : 24, 'marks' : 5}
],
'lyon' : [
    { 'roll' : 24, 'marks' : 12},
    { 'roll' : 24, 'marks' : 11},
    { 'roll' : 24, 'marks' : 19},
    { 'roll' : 24, 'marks' : 5}
],

}

sortedTest = { k: sorted(v, key = lambda x: x['marks']) for k, v in test_dict2.items()}
print(sortedTest)