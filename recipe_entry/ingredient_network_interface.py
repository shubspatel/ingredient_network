from get_compatible_ingredients import compatibility_main
from get_substitutions import substitution_main

functionality = input("Which functionality do you want to access?\n"
                      "0: Ingredient Pairings\n"
                      "1: Ingredient Substitution\n")

if functionality == "0":
    compatibility_main()
elif functionality == "1":
    substitution_main()
else:
    print("Invalid input. Exiting safely!")
