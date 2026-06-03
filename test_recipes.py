from recipes import DietaryRecipe, Ingredient, Recipe, ShoppingList

def test_ingredient_init():
    ingredient = Ingredient("Мука", 500, "г")

    assert ingredient.name == "Мука"
    assert ingredient.quantity == 500.0
    assert ingredient.unit == "г"

def test_ingredient_str():
    ingredient = Ingredient("Мука", 500, "г")

    assert str(ingredient) == "Мука: 500.0 г"

def test_ingredient_eq():
    item1 = Ingredient("Мука", 500, "г")
    item2 = Ingredient("Мука", 1000, "г")
    item3 = Ingredient("Сахар", 500, "г")
    item4 = Ingredient("Мука", 0.5, "кг")

    assert item1 == item2
    assert item1 != item3
    assert item1 != item4

def test_bad_quantity():
    try:
        Ingredient("Мука", -1, "г")

        assert False

    except ValueError:
        assert True

def test_recipe_init():
    ingredients = [Ingredient("Мука", 500, "г")]
    recipe = Recipe("Пирог", ingredients)

    assert recipe.title == "Пирог"
    assert recipe.ingredients == ingredients

def test_add_ingredient():
    recipe = Recipe("Пирог")
    ingredient = Ingredient("Мука", 500, "г")

    recipe.add_ingredient(ingredient)

    assert len(recipe.ingredients) == 1
    assert recipe.ingredients[0] == ingredient

def test_add_same_ingredient():
    recipe = Recipe("Пирог")

    recipe.add_ingredient(Ingredient("Мука", 500, "г"))
    recipe.add_ingredient(Ingredient("Мука", 200, "г"))

    assert len(recipe.ingredients) == 1
    assert recipe.ingredients[0].quantity == 700.0

def test_recipe_scale():
    recipe = Recipe("Пирог", [Ingredient("Мука", 500, "г")])

    scaled = recipe.scale(2)

    assert isinstance(scaled, Recipe)
    assert scaled is not recipe
    assert scaled.ingredients[0].quantity == 1000.0
    assert recipe.ingredients[0].quantity == 500.0

def test_bad_ratio():
    recipe = Recipe("Пирог", [Ingredient("Мука", 500, "г")])

    try:
        recipe.scale(0)

        assert False

    except ValueError:
        assert True

def test_recipe_len():
    recipe = Recipe("Пирог")

    recipe.add_ingredient(Ingredient("Мука", 500, "г"))
    recipe.add_ingredient(Ingredient("Мука", 200, "г"))
    recipe.add_ingredient(Ingredient("Сахар", 100, "г"))

    assert len(recipe) == 2

def test_diet_scale():
    recipe = DietaryRecipe("Каша", "веган", [Ingredient("Овсянка", 100, "г")])

    scaled = recipe.scale(3)

    assert isinstance(scaled, DietaryRecipe)
    assert scaled.diet_type == "веган"
    assert scaled.ingredients[0].quantity == 300.0

def test_diet_str():
    recipe = DietaryRecipe("Каша", "веган", [Ingredient("Овсянка", 100, "г")])

    assert str(recipe) == "[веган] Каша\nОвсянка: 100.0 г"

def test_add_recipe():
    recipe = Recipe("Пирог", [Ingredient("Мука", 500, "г")])
    shop = ShoppingList()

    shop.add_recipe(recipe, 2)
    result = shop.get_list()

    assert len(result) == 1
    assert result[0].name == "Мука"
    assert result[0].quantity == 1000.0

def test_bad_portions():
    recipe = Recipe("Пирог", [Ingredient("Мука", 500, "г")])
    shop = ShoppingList()

    try:
        shop.add_recipe(recipe, 0)

        assert False

    except ValueError:
        assert True

def test_remove_recipe():
    pie = Recipe("Пирог", [Ingredient("Мука", 500, "г")])
    salad = Recipe("Салат", [Ingredient("Огурец", 2, "шт")])

    shop = ShoppingList()

    shop.add_recipe(pie, 1)
    shop.add_recipe(salad, 1)
    shop.remove_recipe("Пирог")

    result = shop.get_list()

    assert len(result) == 1
    assert result[0].name == "Огурец"

def test_remove_missing():
    recipe = Recipe("Пирог", [Ingredient("Мука", 500, "г")])
    shop = ShoppingList()

    shop.add_recipe(recipe, 1)
    shop.remove_recipe("Салат")

    result = shop.get_list()

    assert len(result) == 1

def test_get_list():
    pie = Recipe("Пирог", [Ingredient("Мука", 500, "г")])
    pizza = Recipe("Пицца", [Ingredient("Мука", 300, "г"), Ingredient("Сыр", 200, "г")])

    shop = ShoppingList()

    shop.add_recipe(pie, 1)
    shop.add_recipe(pizza, 1)

    result = shop.get_list()

    assert result[0].name == "Мука"
    assert result[0].quantity == 800.0
    assert result[1].name == "Сыр"

def test_add_lists():
    recipe1 = Recipe("Пирог", [Ingredient("Мука", 500, "г")])
    recipe2 = Recipe("Салат", [Ingredient("Огурец", 2, "шт")])

    list1 = ShoppingList()
    list2 = ShoppingList()

    list1.add_recipe(recipe1, 1)
    list2.add_recipe(recipe2, 1)
    
    new_list = list1 + list2

    assert len(new_list.get_list()) == 2
    assert len(list1.get_list()) == 1
    assert len(list2.get_list()) == 1
