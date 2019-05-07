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

sample_size = 636 # size needed for 95% confidence and +- 5%


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


def _calibrate(seed_ing, total_num_ingredients, scoring_system, percentile, cursor):
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

    threshold_dict = {}

    for val in range(percentile-15, percentile+15, 5):
        test = int(len(score_library) * (val/100))
        threshold_dict[val] = score_library[test]

    print("calibration time: ", time.time()-start_time)
    return threshold_dict


def get_like_ingredients(request, cursor):

    seed_ing = request.seed
    amount_of_ingredients = request.num_ingredients
    scoring_system = request.scoring_system
    threshold = 0

    start_time = time.time()
    total_num_ingredients = _get_num_ingredients(cursor)

    return_list = request.associated_ingredients

    if not request.threshold_library:
        print("Must Calibrate!")
        calibration_counter = 1
        request.threshold_library = _calibrate(seed_ing,
                                               total_num_ingredients,
                                               scoring_system,
                                               request.percentile,
                                               cursor)

        threshold = request.threshold_library[request.percentile]

        while threshold == 0:
            threshold = _calibrate(seed_ing,
                                   total_num_ingredients,
                                   scoring_system,
                                   request.percentile,
                                   cursor)

            calibration_counter += 1

            if calibration_counter == 5:
                return []

        print("Done Calibrating! My threshold score is: ", threshold)

    threshold = request.threshold_library[request.percentile]
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

    request.associated_ingredients = return_list
    print("Compatibility search took: ", time.time()-start_time, "seconds")
    return request
