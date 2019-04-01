

class IngredientsRequest:

    def __init__(self, seed_ingredient, num_ing_desired, scoring_system):
        self.seed = seed_ingredient
        self.num_ingredients = num_ing_desired
        self.scoring_system = scoring_system

        self.percentile = 80
        self.threshold_library = None
        self.associated_ingredients = {}

    def inc_threshold(self):
        if self.percentile < 95:
            self.percentile += 5

    def inc_num_desired_ingredients(self):
        self.num_ingredients += 1

    def clear_ingredients(self):
        self.associated_ingredients = {}
