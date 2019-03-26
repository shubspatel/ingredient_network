from parse_ingredients_from_recipe_file import parse_recipe
import pymysql
import time

file_name = input("enter file name: ")
ing_file_name = input("enter file name of ingredients list: ")

file_name = '/home/user/PycharmProjects/CSCapstone/recipe_entry/data/recipe_data/epicurious-recipes.json'
ing_file_name = '/home/user/PycharmProjects/CSCapstone/recipe_entry/data/ingredients_data/ing_list.json'
parsed_recipes = parse_recipe(file_name, ing_file_name)

connection = pymysql.connect(host='localhost',
                             user='py',
                             password='password',
                             db='ingredients',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

recipe_table = "recipe"
recipe_name_column = "recipe_name"
recipe_id_column = "recipe_ID"

ingredient_table = "ingredient"
ingredient_id_column = "ingredient_ID"
ingredient_name_column = "ingredient_name"

recipe_ingredient_table = "recipe_ingredient"

start_time = time.time()
current_time = time.time()

amount = len(parsed_recipes)
counter = 0

for item in parsed_recipes:

    if time.time() - current_time > 2.5:
        print("still chunking. only: ", (amount-counter), "left")
        current_time = time.time()

    recipe_title = item[0]
    recipe_ingredients = item[1]

    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO {0}({1}) VALUES (%s)".format(recipe_table,
                                                          recipe_name_column)

            cursor.execute(sql, recipe_title)

        connection.commit()

        with connection.cursor() as cursor:
            sql = "SELECT last_insert_id()"
            cursor.execute(sql)
            recipe_id = int(cursor.fetchone()['last_insert_id()'])

        for ing in recipe_ingredients:
            with connection.cursor() as cursor:
                sql = "SELECT {0} FROM {1} WHERE {2} = %s".format(ingredient_id_column,
                                                                  ingredient_table,
                                                                  ingredient_name_column)

                cursor.execute(sql, ing)
                ing_id = int(cursor.fetchone()['ingredient_ID'])

            with connection.cursor() as cursor:
                sql = "INSERT INTO {0}({1}, {2}) VALUES (%s, %s)".format(recipe_ingredient_table,
                                                                         recipe_id_column,
                                                                         ingredient_id_column)

                cursor.execute(sql, (recipe_id, ing_id))

            connection.commit()
    except:
        print(cursor._last_executed)

    counter += 1

connection.close()
print(time.time()-start_time)
