import json
import requests

headers = {"accept": "application/json"}
#In order ot get extended fields, use ?getExtendedFields=true

#Creates and returns a dictionary with category number as the key and category type as the value
def make_category_dict():
    url = "https://api.tcgplayer.com/catalog/categories"

    response = requests.get(url, headers=headers)
    responseJson = response.json()
    responseResults = responseJson['results']

    categoryList = {}
    for category in responseResults:
        categoryList[category['categoryId']] = category['name']

    return categoryList


#Gets all category groups (includes sets) based off category id
def get_category_groups(id):
    if not id.isnumeric():
        print("You have inputted a non-numeric category id.")
        print("Your input was: " + str(id))
        return

    url = "https://api.tcgplayer.com/catalog/categories/categoryId/groups/" + str(id)
    response = requests.get(url, headers = headers)
    responseJson = response.json()
    responseResults = responseJson['results']
    for group in responseResults:

