from score_functions import cs_from_shared_recipes_strict
from score_functions import cs_from_shared_recipes_lenient
from score_functions import cs_from_ing_neighbors_strict
from score_functions import cs_from_ing_neighbors_lenient
from score_functions import ss_from_ing_neighbors
from score_functions import cs_from_shared_recipes_over_total_strict
from score_functions import cs_from_shared_recipes_over_total_lenient
from score_functions import cs_from_ing_neighbors_in_shared_recipes_lenient
from score_functions import cs_from_ing_neighbors_in_shared_recipes_strict
import pymysql
import sys

connection = pymysql.connect(host='localhost',
                             user='py',
                             password='password',
                             db='ingredients',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

ing_a = input("What's the first ingredient?").strip()
ing_b = input("What's the second ingredient?").strip()

try:
    with connection.cursor() as cursor:
        shared_score = cs_from_shared_recipes_strict(ing_a, ing_b, cursor)
        shared_score_lenient = cs_from_shared_recipes_lenient(ing_a, ing_b, cursor)
        ing_neighbors_score = cs_from_ing_neighbors_strict(ing_a, ing_b, cursor)
        ing_neighbors_score_lenient = cs_from_ing_neighbors_lenient(ing_a, ing_b, cursor)
        ing_neighbors_score_exp = ss_from_ing_neighbors(ing_a, ing_b, cursor)
        ing_neighbors_score_shared_strict = cs_from_ing_neighbors_in_shared_recipes_strict(ing_a, ing_b, cursor)
        ing_neighbors_score_shared_lenient = cs_from_ing_neighbors_in_shared_recipes_lenient(ing_a, ing_b, cursor)
        shared_score_over_total = cs_from_shared_recipes_over_total_strict(ing_a, ing_b, cursor)
        shared_score_over_total_lenient = cs_from_shared_recipes_over_total_lenient(ing_a, ing_b, cursor)

        print("Compatibility score from shared recipes (strict): {}".format(shared_score))
        print("Compatibility score from shared recipes (lenient): {}".format(shared_score_lenient))
        print("Compatibility score from Ingredient Neighbors (strict): {}".format(ing_neighbors_score))
        print("Compatibility score from Ingredient Neighbors (lenient): {}".format(ing_neighbors_score_lenient))
        print("Substitutability score from Ingredient Neighbors (experimental): {}".format(ing_neighbors_score_exp))
        print("Compatibility score from Ingredient Neighbors in Shared Recipes (strict): {}".format(ing_neighbors_score_shared_strict))
        print("Compatibility score from Ingredient Neighbors in Shared Recipes (lenient): {}".format(ing_neighbors_score_shared_lenient))
        print("Compatibility score from shared recipes over all recipes participated in (strict): {}".format(shared_score_over_total))
        print("Compatibility score from shared recipes over all recipes participated in (lenient): {}".format(shared_score_over_total_lenient))
except:
    print ("Unexpected error:", sys.exc_info()[0])
    print(cursor._last_executed)

connection.close()
