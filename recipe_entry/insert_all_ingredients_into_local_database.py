import pymysql.cursors
import simplejson as json
import time

connection = pymysql.connect(host='localhost',
                             user='py',
                             password='password',
                             db='ingredients',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


ing_file_name = "/home/user/PycharmProjects/CSCapstone/recipe_entry/data/ingredients_data/ing_list.json"
table_name = "ingredient"
column_name = "ingredient_name"

with open(ing_file_name) as ing:
    master_ingredients_table = json.loads(ing.read())

start_time = time.time()
for item in master_ingredients_table:
    try:
        with connection.cursor() as cursor:

            #sql = "INSERT INTO ingredient(ingredient_name) VALUES (%s)"
            sql = "INSERT INTO {0} ({1}) " \
                  "SELECT * FROM (SELECT %s) AS tmp " \
                  "WHERE NOT EXISTS (" \
                  "SELECT {2} FROM {3} WHERE {4} = %s) LIMIT 1".format(table_name,
                                                                       column_name,
                                                                       column_name,
                                                                       table_name,
                                                                       column_name,
                                                                       )
            cursor.execute(sql, (item, item))

        connection.commit()
    except:
        print(cursor._last_executed)


connection.close()
print(time.time()-start_time)
