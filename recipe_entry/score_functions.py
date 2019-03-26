

def _get_how_many_times_appears_strict(ing, cursor):
    sql = "SELECT count(*) as c " \
          "FROM recipe " \
          "INNER JOIN recipe_ingredient ON recipe.recipe_ID = recipe_ingredient.recipe_ID " \
          "INNER JOIN ingredient on recipe_ingredient.ingredient_ID = ingredient.ingredient_ID " \
          "WHERE ingredient_name = %s"

    cursor.execute(sql, (ing))
    return cursor.fetchone()['c']


def _get_how_many_times_appears_lenient(ing, cursor):
    sql = "SELECT count(*) as c " \
          "FROM recipe " \
          "INNER JOIN recipe_ingredient ON recipe.recipe_ID = recipe_ingredient.recipe_ID " \
          "INNER JOIN ingredient on recipe_ingredient.ingredient_ID = ingredient.ingredient_ID " \
          "WHERE ingredient_name LIKE %s"

    cursor.execute(sql, ("%"+ing+"%"))
    return cursor.fetchone()['c']


def _get_how_many_times_appear_together(ing_a_ID, ing_b_ID, cursor):
    sql = "SELECT rec_ing.ingredient_id, rec_ing2.ingredient_id, count(*) AS c " \
          "FROM recipe_ingredient rec_ing JOIN recipe_ingredient rec_ing2 " \
          "ON rec_ing.recipe_ID = rec_ing2.recipe_ID " \
          "WHERE rec_ing.ingredient_ID = %s AND rec_ing2.ingredient_ID = %s"

    cursor.execute(sql, (ing_a_ID, ing_b_ID))
    return cursor.fetchone()['c']


def _fetch_ing_id_strict(ing, cursor):
    sql = "SELECT ingredient_ID from ingredient WHERE ingredient_name = %s"
    cursor.execute(sql, (ing))

    return cursor.fetchone()['ingredient_ID']


def _fetch_ing_id_lenient(ing, cursor):
    sql = "SELECT ingredient_ID from ingredient WHERE ingredient_name LIKE %s"
    cursor.execute(sql, ("%" + ing + "%"))

    return cursor.fetchall()


def _fetch_all_recipes_ing_is_in_strict(ing, cursor):
    sql = "SELECT recipe_ID FROM recipe_ingredient " \
          "JOIN ingredient ON " \
          "recipe_ingredient.ingredient_ID = ingredient.ingredient_ID " \
          "WHERE ingredient.ingredient_name = %s"

    cursor.execute(sql, (ing))

    return cursor.fetchall()


def _fetch_all_recipes_ing_is_in_lenient(ing, cursor):
    sql = "SELECT recipe_ID FROM recipe_ingredient " \
          "JOIN ingredient ON " \
          "recipe_ingredient.ingredient_ID = ingredient.ingredient_ID " \
          "WHERE ingredient.ingredient_name LIKE %s"

    cursor.execute(sql, ("%"+ing+"%"))

    return cursor.fetchall()


def _fetch_ingredients_in_recipe(recipe_ID, cursor):
    sql = "SELECT ingredient_ID FROM recipe_ingredient WHERE recipe_ID = %s"
    cursor.execute(sql, (recipe_ID))

    return cursor.fetchall()


def cs_from_shared_recipes_strict(ing_a, ing_b, cursor):
    ing_a_ID = _fetch_ing_id_strict(ing_a, cursor)
    ing_b_ID = _fetch_ing_id_strict(ing_b, cursor)

    together_count = _get_how_many_times_appear_together(ing_a_ID, ing_b_ID, cursor)

    return together_count


def cs_from_shared_recipes_lenient(ing_a, ing_b, cursor):
    ing_a_ID_dict_list = _fetch_ing_id_lenient(ing_a, cursor)
    ing_b_ID_dict_list = _fetch_ing_id_lenient(ing_b, cursor)

    def _get_ID_list(dict_list):
        ing_ID_list = set()
        for item in dict_list:
            if item['ingredient_ID'] not in ing_ID_list:
                ing_ID_list.add(item['ingredient_ID'])

        return ing_ID_list

    ing_a_ID_list = _get_ID_list(ing_a_ID_dict_list)
    ing_b_ID_list = _get_ID_list(ing_b_ID_dict_list)

    together_count = 0
    for a_ID in ing_a_ID_list:
        for b_ID in ing_b_ID_list:
            together_count += _get_how_many_times_appear_together(a_ID, b_ID, cursor)

    return together_count


def cs_from_ing_neighbors_strict(ing_a, ing_b, cursor):
    ing_a_recipe_list = _fetch_all_recipes_ing_is_in_strict(ing_a, cursor)
    ing_b_recipe_list = _fetch_all_recipes_ing_is_in_strict(ing_b, cursor)

    def _extract_recipe_IDs(recipe_list):
        recipe_IDs = set()
        for item in recipe_list:
            if item['recipe_ID'] not in recipe_IDs:
                recipe_IDs.add(item['recipe_ID'])

        return recipe_IDs

    a_recipe_IDs_list = _extract_recipe_IDs(ing_a_recipe_list)
    b_recipe_IDs_list = _extract_recipe_IDs(ing_b_recipe_list)

    def _extract_ing_neighbors(recipe_IDs_list):
        neighbors = set()

        for recipe_ID in recipe_IDs_list:
            neighbors_list = _fetch_ingredients_in_recipe(recipe_ID, cursor)
            for item in neighbors_list:
                if item['ingredient_ID'] not in neighbors:
                    neighbors.add(item['ingredient_ID'])

        return neighbors

    a_neighbors = _extract_ing_neighbors(a_recipe_IDs_list)
    b_neighbors = _extract_ing_neighbors(b_recipe_IDs_list)

    return len(a_neighbors.intersection(b_neighbors))


def cs_from_ing_neighbors_lenient(ing_a, ing_b, cursor):
    ing_a_recipe_list = _fetch_all_recipes_ing_is_in_lenient(ing_a, cursor)
    ing_b_recipe_list = _fetch_all_recipes_ing_is_in_lenient(ing_b, cursor)

    def _extract_recipe_IDs(recipe_list):
        recipe_IDs = set()
        for item in recipe_list:
            if item['recipe_ID'] not in recipe_IDs:
                recipe_IDs.add(item['recipe_ID'])

        return recipe_IDs

    a_recipe_IDs_list = _extract_recipe_IDs(ing_a_recipe_list)
    b_recipe_IDs_list = _extract_recipe_IDs(ing_b_recipe_list)

    def _extract_ing_neighbors(recipe_IDs_list):
        neighbors = set()

        for recipe_ID in recipe_IDs_list:
            neighbors_list = _fetch_ingredients_in_recipe(recipe_ID, cursor)
            for item in neighbors_list:
                if item['ingredient_ID'] not in neighbors:
                    neighbors.add(item['ingredient_ID'])

        return neighbors

    a_neighbors = _extract_ing_neighbors(a_recipe_IDs_list)
    b_neighbors = _extract_ing_neighbors(b_recipe_IDs_list)

    return len(a_neighbors.intersection(b_neighbors))


def ss_from_ing_neighbors(ing_a, ing_b, cursor):
    ing_a_recipe_list = _fetch_all_recipes_ing_is_in_strict(ing_a, cursor)
    ing_b_recipe_list = _fetch_all_recipes_ing_is_in_strict(ing_b, cursor)

    def _extract_recipe_IDs(recipe_list):
        recipe_IDs = set()
        for item in recipe_list:
            if item['recipe_ID'] not in recipe_IDs:
                recipe_IDs.add(item['recipe_ID'])

        return recipe_IDs

    a_recipe_IDs_list = _extract_recipe_IDs(ing_a_recipe_list)
    b_recipe_IDs_list = _extract_recipe_IDs(ing_b_recipe_list)

    IDs_to_remove = a_recipe_IDs_list.intersection(b_recipe_IDs_list)

    a_recipe_IDs_list -= IDs_to_remove
    b_recipe_IDs_list -= IDs_to_remove

    def _extract_ing_neighbors(recipe_IDs_list):
        neighbors = set()

        for recipe_ID in recipe_IDs_list:
            neighbors_list = _fetch_ingredients_in_recipe(recipe_ID, cursor)
            for item in neighbors_list:
                if item['ingredient_ID'] not in neighbors:
                    neighbors.add(item['ingredient_ID'])

        return neighbors

    a_neighbors = _extract_ing_neighbors(a_recipe_IDs_list)
    b_neighbors = _extract_ing_neighbors(b_recipe_IDs_list)

    return len(a_neighbors.intersection(b_neighbors))


def cs_from_ing_neighbors_in_shared_recipes_strict(ing_a, ing_b, cursor):
    ing_a_recipe_list = _fetch_all_recipes_ing_is_in_strict(ing_a, cursor)
    ing_b_recipe_list = _fetch_all_recipes_ing_is_in_strict(ing_b, cursor)

    def _extract_recipe_IDs(recipe_list):
        recipe_IDs = set()
        for item in recipe_list:
            if item['recipe_ID'] not in recipe_IDs:
                recipe_IDs.add(item['recipe_ID'])

        return recipe_IDs

    a_recipe_IDs_list = _extract_recipe_IDs(ing_a_recipe_list)
    b_recipe_IDs_list = _extract_recipe_IDs(ing_b_recipe_list)

    IDs_to_check = a_recipe_IDs_list.intersection(b_recipe_IDs_list)

    def _extract_ing_neighbors(recipe_IDs_list):
        neighbors = set()

        for recipe_ID in recipe_IDs_list:
            neighbors_list = _fetch_ingredients_in_recipe(recipe_ID, cursor)
            for item in neighbors_list:
                if item['ingredient_ID'] not in neighbors:
                    neighbors.add(item['ingredient_ID'])

        return neighbors

    neighbors = _extract_ing_neighbors(IDs_to_check)

    return len(neighbors)


def cs_from_ing_neighbors_in_shared_recipes_lenient(ing_a, ing_b, cursor):
    ing_a_recipe_list = _fetch_all_recipes_ing_is_in_lenient(ing_a, cursor)
    ing_b_recipe_list = _fetch_all_recipes_ing_is_in_lenient(ing_b, cursor)

    def _extract_recipe_IDs(recipe_list):
        recipe_IDs = set()
        for item in recipe_list:
            if item['recipe_ID'] not in recipe_IDs:
                recipe_IDs.add(item['recipe_ID'])

        return recipe_IDs

    a_recipe_IDs_list = _extract_recipe_IDs(ing_a_recipe_list)
    b_recipe_IDs_list = _extract_recipe_IDs(ing_b_recipe_list)

    IDs_to_check = a_recipe_IDs_list.intersection(b_recipe_IDs_list)

    def _extract_ing_neighbors(recipe_IDs_list):
        neighbors = set()

        for recipe_ID in recipe_IDs_list:
            neighbors_list = _fetch_ingredients_in_recipe(recipe_ID, cursor)
            for item in neighbors_list:
                if item['ingredient_ID'] not in neighbors:
                    neighbors.add(item['ingredient_ID'])

        return neighbors

    neighbors = _extract_ing_neighbors(IDs_to_check)

    return len(neighbors)


def cs_from_shared_recipes_over_total_strict(ing_a, ing_b, cursor):
    a_recipe_count = _get_how_many_times_appears_strict(ing_a, cursor)
    b_recipe_count = _get_how_many_times_appears_strict(ing_b, cursor)

    together_count = cs_from_shared_recipes_strict(ing_a, ing_b, cursor)
    return together_count / (a_recipe_count + b_recipe_count)


def cs_from_shared_recipes_over_total_lenient(ing_a, ing_b, cursor):
    a_recipe_count = _get_how_many_times_appears_lenient(ing_a, cursor)
    b_recipe_count = _get_how_many_times_appears_lenient(ing_b, cursor)

    together_count = cs_from_shared_recipes_lenient(ing_a, ing_b, cursor)
    return together_count / (a_recipe_count + b_recipe_count)
