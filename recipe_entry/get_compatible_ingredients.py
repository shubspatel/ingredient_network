import pymysql
import sys
from compatible_ingredients import get_like_ingredients

connection = pymysql.connect(host='localhost',
                             user='py',
                             password='password',
                             db='ingredients',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

seed_ing = input("What's the seed ingredient?")
num_ingredients = int(input("How many ingredients do you want?"))
scoring_system = input("Which scoring system is desired? View below for options.\n "
                       "0:cs_from_shared_recipes_strict \n"
                       "1:cs_from_shared_recipes_lenient \n"
                       "2:cs_from_ing_neighbors_strict \n"
                       "3:cs_from_ing_neighbors_lenient \n"
                       "4:cs_from_ing_neighbors_in_shared_recipes_strict \n"
                       "5:cs_from_ing_neighbors_in_shared_recipes_lenient \n"
                       "6:cs_from_shared_recipes_over_total_strict \n"
                       "7:cs_from_shared_recipes_over_total_lenient\n")

scoring_system = int(scoring_system)

with connection.cursor() as cursor:
        retVal = get_like_ingredients(seed_ing, num_ingredients, scoring_system, cursor)

        if not retVal:
            print("No ingredients found! Maybe too low a threshold?")
        else:
            print(retVal)

connection.close()
