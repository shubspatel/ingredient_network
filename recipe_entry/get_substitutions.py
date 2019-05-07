import pymysql
import random
import time
from SubstitutionRequest import SubstitutionRequest
from score_functions import ss_from_ing_neighbors


calibration_dictionary = {}


def _exit(connection):
    try:
        connection.close()
    except:
        raise Exception


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


def _calibrate(seed_ing, total_num_ingredients, percentile, cursor):
    sample_size = 636 # number required for 95% confidence is 636
    start_time = time.time()
    print("Beginning Calibration!")

    if seed_ing in calibration_dictionary:
        print("Calibration was done previously!")
        return calibration_dictionary[seed_ing]

    score_library = []
    used_IDs = set()
    rand_id = 0

    for i in range(sample_size):
        print("Calibrating! Only", sample_size-i, "samples left")
        used_IDs.add(rand_id)
        while rand_id in used_IDs:
            rand_id = random.randint(1, total_num_ingredients)

        rand_ing = _get_ing_name(rand_id, cursor)

        score = ss_from_ing_neighbors(rand_ing, seed_ing, cursor)

        if score is not 0:
            score_library.append(score)

    score_library.sort()

    threshold = score_library[int(len(score_library) * percentile/100)]

    print("calibration time: ", time.time()-start_time)
    calibration_dictionary[seed_ing] = threshold
    return threshold


def _recurring_instructions(connection):
    functionality = input("What do you want to do? \n"
                          "0: Find a substitute for an ingredient \n"
                          "1: See if two ingredients can be substituted for each other \n")

    if functionality == "0":
        _find_substitute(connection)
        _recurring_instructions(connection)
    elif functionality == "1":
        _check_substitutes(connection)
        _recurring_instructions(connection)
    else:
        print("Invalid input. Exiting safely!")
        exit()


def _get_substitute(request, cursor):
    total_num_ingredients = _get_num_ingredients(cursor)
    threshold = int(_calibrate(request.seed, total_num_ingredients, 93, cursor))

    loop_timer = time.time()
    retVal = None

    used_IDs = set()
    rand_id = 0
    score = 0
    attempts = 0
    attempt_limit = 100
    best = None
    best_score = 0

    while retVal is None:
        attempts += 1
        if attempts > attempt_limit:
            retVal = best
            score = best_score
            break

        if time.time() - loop_timer > 2:
            print("Still searching for substitute!")
            loop_timer = time.time()

        used_IDs.add(rand_id)
        while rand_id in used_IDs:
            rand_id = random.randint(1, total_num_ingredients)

        rand_ing = _get_ing_name(rand_id, cursor)

        score = ss_from_ing_neighbors(rand_ing, request.seed, cursor)

        if score >= threshold:
            retVal = rand_ing

        if score >= best_score:
            best = rand_ing
            best_score = score

    return best, best_score, threshold


def _find_substitute(connection):
    seed_ing = input("What ingredient do you want a substitute for?\n")
    request = SubstitutionRequest(seed_ing)

    with connection.cursor() as cursor:
            retVal, score, threshold = _get_substitute(request, cursor)

            print("Try substituting with {}. It has a score of {} and the threshold was {}".format(retVal,
                                                                                                   score,
                                                                                                   threshold))


def _check_substitutes(connection):
    ing_a = input("What is the original ingredient?\n")
    ing_b = input("What is the substitute?\n")
    with connection.cursor() as cursor:
        threshold= _calibrate(ing_a, _get_num_ingredients(cursor), 98, cursor)
        score = ss_from_ing_neighbors(ing_a, ing_b, cursor)
        print("The substitution score is: {}".format(score))
        print("The threshold score for {} is: {}".format(ing_a, threshold))
        if score > threshold:
            print("The score is greater than the threshold, so it's a good substitute!")
        else:
            print("The score is below the threshold, so it might not be the best substitute!")


def substitution_main():
    # set up connection
    connection = pymysql.connect(host='localhost',
                                 user='py',
                                 password='password',
                                 db='ingredients',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    _recurring_instructions(connection)

    _exit(connection)
