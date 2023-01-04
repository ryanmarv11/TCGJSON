import json
import requests

headers = {"accept": "application/json"}


# In order ot get extended fields, use ?getExtendedFields=true

# Creates and returns a dictionary with category number as the key and category type as the value
def make_category_dict():
    url = "https://api.tcgplayer.com/catalog/categories"

    response = requests.get(url, headers=headers)
    responseJson = response.json()
    responseResults = responseJson['results']

    categoryList = {}
    for category in responseResults:
        categoryList[category['categoryId']] = category['name']

    return categoryList


# Gets all category groups (includes sets) based off category id
def get_category_groups(categoryId):
    #Verifies that the cateogyrId is a positive integer
    if not categoryId.isnumeric() or categoryId <= 0:
        print("You have inputted an category id.")
        print("Your input was: " + str(categoryId))
        print("A categoryId must be a positive integer")
        return

    url = "https://api.tcgplayer.com/catalog/categories/categoryId/groups/" + str(categoryId)
    response = requests.get(url, headers=headers)
    responseJson = response.json()
    responseResults = responseJson['results']

    categoryGroupDict = {}
    for group in responseResults:
        categoryGroupDict[group['groupId']] = group
    return categoryGroupDict


# Gets all products based on groupId
def get_group_products(groupId):
    #Verifies that the groupId is a number
    if not groupId.isNumeric() or groupId <= 0:
        print("You have inputted a non-numeric category id.")
        print("Your input was: " + str(groupId))
        print("groupId must be a positive integer")
        return

    url = "https://api.tcgplayer.com/catalog/products?groupId=" + str(groupId) + "&getExtendedFields=true"
    response = requests.get(url, headers=headers)
    responseJson = response.json()
    responseResults = responseJson['results']

    groupProductList = {}
    for product in responseResults:
        groupProductList[product['name']] = product
    return groupProductList

