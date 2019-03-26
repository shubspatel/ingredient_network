import simplejson as json

file_name = input("enter file name: ")

with open(file_name) as f:
    x = 0
    json_data = json.loads(f.read())

    ingredients_list = {}
    for item in json_data:
        ing_list = item['ingredients']
        for val in ing_list:
            ingredients_list[val.lower()] = None

ingredients_list_json_file = input("where do you want to put the new file? ")

with open(ingredients_list_json_file, 'w') as file:
    json.dump(ingredients_list, file)
