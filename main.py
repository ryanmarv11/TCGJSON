import json
import requests

headers = {"accept": "application/json"}


# In order ot get extended fields, use ?getExtendedFields=true for product and group calls

# Returns a dictionary with category number as the key and category type as the value
def make_category_dict():
    url = "https://api.tcgplayer.com/catalog/categories"

    response = requests.get(url, headers=headers)
    if response.status_code == 404:
        print("ERROR: Categories were unable to be retrieved. Here is the raw")
        print(response.raw)
        return
    responseJson = response.json()
    responseResults = responseJson['results']

    categoryList = {}
    for category in responseResults:
        categoryList[category['categoryId']] = category['name']

    return categoryList


# Returns dictionary of category groups (keys are groupId, values are group information) based on integer categoryId
def get_category_groups(categoryId):
    # Verifies that the cateogyrId is a positive integer
    if not categoryId.isnumeric() or categoryId <= 0:
        print("You have inputted an category id.")
        print("Your input was: " + str(categoryId))
        print("A categoryId must be a positive integer")
        return

    url = "https://api.tcgplayer.com/catalog/categories/" + str(categoryId) + "/groups/"
    response = requests.get(url, headers=headers)
    if response.status_code == 404:
        print("ERROR: No category or groups were found with categoryId of " + str(categoryId))
        return
    responseJson = response.json()
    responseResults = responseJson['results']

    categoryGroupDict = {}
    for group in responseResults:
        categoryGroupDict[group['groupId']] = group
    return categoryGroupDict


# Gets all products based on integer groupId
def get_group_products(groupId):
    # Verifies that the groupId is a number
    if not groupId.isNumeric() or groupId <= 0:
        print("You have inputted a non-numeric category id.")
        print("Your input was: " + str(groupId))
        print("groupId must be a positive integer")
        return

    url = "https://api.tcgplayer.com/catalog/products?groupId=" + str(groupId) + "&getExtendedFields=true"
    response = requests.get(url, headers=headers)
    if response.status_code == 404:
        print("Error: No products found with a groupId of" + str(groupId))
        return
    elif response.status_code == 207:
        print("WARNING: Operation successfully completed but some were missing")

    responseJson = response.json()
    responseResults = responseJson['results']

    groupProductList = {}
    for product in responseResults:
        groupProductList[product['productId']] = product
    return groupProductList


# From list of productId's creates a string of productId's separated by commas for API call
def product_list_translate(productList):
    productString = ""
    for product in productList.keys():
        productString += str(product) + ','
    return productString[:-1]


# Based on a list of productId's returns a dictionary with the name as key and relevant information as values
# Information will vary based off the card game
def make_product_dict(productIds):
    url = "https://api.tcgplayer.com/catalog/products/productIds"
    response = requests.get(url, headers=headers)
    responseJson = response.json()
    responseResults = responseJson['results']
    productDict = {}
    for product in responseResults:
        # this is where the specifics would come in
        productDict[product['name']] = product['productId']
    return productDict


def main():
    categoryDict = make_category_dict()
    for key in categoryDict.keys():
        print("[" + str(key) + "]\t" + categoryDict[key])

    categoryId = int(input("What categoryId would you like to get groups for? (Positive integers only)"))
    while not categoryId.isnumeric():
        print("ERROR: You have not input a number.")
        categoryId = int(input("What categoryId would you like to get groups for? (Positive integers only)"))

    categoryGroups = get_category_groups(categoryId)
    for key in categoryGroups.keys():
        print("[" + str(key) + "]\t" + categoryGroups[key])

    groupId = int(input("What groupId would you like to get groups for? (Positive integers only)"))
    while not groupId.isnumeric():
        print("ERROR: You have not input a number.")
        groupId = int(input("What groupId would you like to get groups for? (Positive integers only)"))

    groupProducts = get_group_products(groupId)
    productIdList = product_list_translate(groupProducts)

    productDict = make_product_dict(productIdList)
    while True:
        fileName = input("What would you like the file name to be?")
        print("You have entered " + fileName + " is that correct")
        fileNameCheck = input("Y/N")
        if fileNameCheck == "Y":
            break
    fileName += '.json'
    json.dump(productDict, fileName)
