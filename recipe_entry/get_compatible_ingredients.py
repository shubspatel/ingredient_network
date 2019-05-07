import pymysql
import sys
from compatible_ingredients import get_like_ingredients
from IngredientsRequest import IngredientsRequest


def _initialize():
    seed_ing = input("What's the seed ingredient?")
    num_ingredients = int(input("How many ingredients do you want?"))
    scoring_system = input("Which scoring system is desired? View below for options.\n"
                           "0:cs_from_shared_recipes_strict \n"
                           "1:cs_from_shared_recipes_lenient \n"
                           "2:cs_from_ing_neighbors_strict \n"
                           "3:cs_from_ing_neighbors_lenient \n"
                           "4:cs_from_ing_neighbors_in_shared_recipes_strict \n"
                           "5:cs_from_ing_neighbors_in_shared_recipes_lenient \n"
                           "6:cs_from_shared_recipes_over_total_strict \n"
                           "7:cs_from_shared_recipes_over_total_lenient\n"
                           "Enter an empty string for default (recommended)\n")

    if not scoring_system.strip():
        scoring_system = 5

    scoring_system = int(scoring_system)
    return IngredientsRequest(seed_ing, num_ingredients, scoring_system)


def _get_associated_ingredients(ingredients_request, connection):
    with connection.cursor() as cursor:
            retVal = get_like_ingredients(ingredients_request, cursor).associated_ingredients

            if not retVal:
                print("No ingredients found! Maybe too high a threshold?")
            else:
                print("Try these ingredients!: ", ", ".join(retVal.keys()))


def _exit(connection):
    try:
        connection.close()
    except:
        raise Exception


def _recurring_instructions(ingredients_request, connection):
    next_instruction = input("What next?\n"
                             "1: Search again (same seed ingredient)\n"
                             "2: Search again with a higher threshold\n"
                             "3: Get one more ingredient\n"
                             "4: Search again (different seed ingredient)\n"
                             "Put any other input to exit.\n")

    if next_instruction == "1":
        ingredients_request.clear_ingredients()
        _get_associated_ingredients(ingredients_request, connection)
        _recurring_instructions(ingredients_request, connection)
    elif next_instruction == "2":
        ingredients_request.inc_threshold()
        ingredients_request.clear_ingredients()
        _get_associated_ingredients(ingredients_request, connection)
        _recurring_instructions(ingredients_request, connection)
    elif next_instruction == "3":
        ingredients_request.inc_num_desired_ingredients()
        _get_associated_ingredients(ingredients_request, connection)
        _recurring_instructions(ingredients_request, connection)
    elif next_instruction == "4":
        _exit(connection)
        compatibility_main()
    else:
        _exit(connection)

    return


def compatibility_main():

    # set up connection
    connection = pymysql.connect(host='localhost',
                                 user='py',
                                 password='password',
                                 db='ingredients',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    ingredients_request = _initialize()

    _get_associated_ingredients(ingredients_request, connection)

    _recurring_instructions(ingredients_request, connection)
