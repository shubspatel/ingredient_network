from score_functions import *
import random
import time

score_factory= {0:cs_from_shared_recipes_strict,
                1:cs_from_shared_recipes_lenient,
                2:cs_from_ing_neighbors_strict,
                3:cs_from_ing_neighbors_lenient,
                4:cs_from_ing_neighbors_in_shared_recipes_strict,
                5:cs_from_ing_neighbors_in_shared_recipes_lenient,
                6:cs_from_shared_recipes_over_total_strict,
                7:cs_from_shared_recipes_over_total_lenient}

sample_size = 100
percentile = 0.8


def _get_num_ingredients(cursor):
    sql = "SELECT count(*) as c " \
          "FROM ingredient"

    cursor.execute(sql)
    return cursor.fetchone()['c']


def _get_ing_name(ing_ID, cursor):
    sql = "SELECT ingredient_name AS name " \
          "FROM ingredient " \
          "WHERE ingredient_ID = %s"

    cursor.execute(sql, (ing_ID))
    return cursor.fetchone()['name']


def _calibrate(seed_ing, total_num_ingredients, scoring_system, cursor):
    start_time = time.time()
    print("Beginning Calibration!")
    score_library = []
    used_IDs = set()
    rand_id = 0

    for i in range(sample_size):
        print("Calibrating! Only", sample_size-i, "samples left")
        used_IDs.add(rand_id)
        while rand_id in used_IDs:
            rand_id = random.randint(1, total_num_ingredients)

        rand_ing = _get_ing_name(rand_id, cursor)

        score = score_factory[scoring_system](rand_ing, seed_ing, cursor)

        if score is not 0:
            score_library.append(score)

    score_library.sort()
    value_to_choose = int(len(score_library) * percentile)

    print("calibration time: ", time.time()-start_time)
    return score_library[value_to_choose]


def get_like_ingredients(seed_ing, amount_of_ingredients, scoring_system, cursor):

    start_time = time.time()
    total_num_ingredients = _get_num_ingredients(cursor)

    return_list = {}

    calibration_counter = 1
    threshold = _calibrate(seed_ing, total_num_ingredients, scoring_system, cursor)

    while threshold == 0:
        threshold = _calibrate(seed_ing, total_num_ingredients, scoring_system, cursor)
        calibration_counter += 1

        if calibration_counter == 5:
            return []

    print("Done Calibrating! My threshold score is: ", threshold)

    used_IDs = set()
    rand_id = 0

    loop_timer = time.time()
    while len(return_list) < amount_of_ingredients:
        if time.time()-loop_timer > 2:
            print("Still searching for ingredients! Currently have: ", len(return_list))
            loop_timer = time.time()

        used_IDs.add(rand_id)
        while rand_id in used_IDs:
            rand_id = random.randint(1, total_num_ingredients)

        rand_ing = _get_ing_name(rand_id, cursor)

        score = score_factory[scoring_system](rand_ing, seed_ing, cursor)

        if score >= threshold:
            return_list[rand_ing] = score

    print("Compatibility search took: ", time.time()-start_time, "seconds")
    return return_list
