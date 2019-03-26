import simplejson as json
import time


def get_windows(l):
    for w in range(1, len(l) + 1):
        for i in range(len(l)-w+1):
            yield l[i:i+w]


def parse_recipe(file_name, ing_file_name):

    title_string = 'title'
    if "epicurious" in file_name:
        title_string = 'hed'

    ret = []
    with open(ing_file_name) as ing:
        master_ingredients_table = json.loads(ing.read())

    time_start = time.time()
    with open(file_name) as f:
        for line in f:
            try:
                parsed_json = json.loads(line)
                ingredient_list = parsed_json['ingredients']

                ingredients_in_this_recipe = []
                for item in ingredient_list:
                    temp_list = item.split()
                    sliding_windows = []
                    windows_generator = get_windows(temp_list)

                    for i in windows_generator:
                        sliding_windows.append(i)

                    sliding_windows.reverse()

                    for i in sliding_windows:
                        if " ".join(i).strip(",") in master_ingredients_table:

                            ingredients_in_this_recipe.append(" ".join(i).strip(","))
                            break

                #print(parsed_json['title'] + " contains: " + ", ".join(ingredients_in_this_recipe))
                ret.append((parsed_json[title_string], ingredients_in_this_recipe))
            except KeyError:
                print("There was a key error. Are you sure there are ingredients in: " + parsed_json[title_string])
                print(parsed_json)

    print(time.time()-time_start)
    return ret


def _main():
    file_name = input("enter file name: ")
    ing_file_name = input("enter file name of ingredients list: ")
    ret = parse_recipe(file_name, ing_file_name)
    print(len(ret))