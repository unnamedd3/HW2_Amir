from recipes import DietaryRecipe, Ingredient, Recipe, ShoppingList

def print_line():
    print("=" * 35)

def print_result(title):
    print()
    print_line()
    print(title)
    print_line()

def print_menu():
    print_line()
    print("ГЛАВНОЕ МЕНЮ")
    print_line()

    print("1. Новый рецепт")
    print("2. Список рецептов")
    print("3. Добавить продукт")
    print("4. Рассчитать порции")
    print("5. Отправить рецепт в покупки")
    print("6. Мои покупки")
    print("0. Завершить работу")

def print_recipes(recipes):
    if len(recipes) == 0:
        print("Пока нет ни одного рецепта.")

    else:
        for i in range(len(recipes)):
            print(str(i + 1) + ") " + recipes[i].title)

def print_recipe(recipe):
    print("Название:", recipe.title)

    if isinstance(recipe, DietaryRecipe):
        print("Тип питания:", recipe.diet_type)

    if len(recipe.ingredients) == 0:
        print("Ингредиенты пока не добавлены.")

    else:
        print("Ингредиенты:")

        for ingredient in recipe.ingredients:
            print("-", ingredient)

def create_recipe(recipes):
    print_result("НОВЫЙ РЕЦЕПТ")

    title = input("Как называется блюдо? ")

    if title == "":
        print("Название не может быть пустым.")

        return

    diet_type = input("Тип питания, если есть (можно оставить пустым): ")

    if diet_type == "":
        recipe = Recipe(title)

    else:
        recipe = DietaryRecipe(title, diet_type)

    recipes.append(recipe)
    print("Готово, рецепт сохранен.")

def add_ingredient_to_recipe(recipes):
    print_result("ДОБАВЛЕНИЕ ПРОДУКТА")
    print_recipes(recipes)

    if len(recipes) == 0:
        return

    number = int(input("Куда добавить продукт? Введите номер: "))

    if number < 1 or number > len(recipes):
        print("Рецепта с таким номером нет.")

        return

    name = input("Продукт: ")

    if name == "":
        print("Название продукта не может быть пустым.")

        return

    quantity = float(input("Сколько нужно? "))
    unit = input("Единицы измерения: ")

    if unit == "":
        print("Единицы измерения не могут быть пустыми.")

        return

    try:
        ingredient = Ingredient(name, quantity, unit)
        recipes[number - 1].add_ingredient(ingredient)

        print("Продукт добавлен в рецепт.")

    except ValueError:
        print("Количество должно быть положительным.")

def show_all_recipes(recipes):
    print_result("ВАШИ РЕЦЕПТЫ")

    if len(recipes) == 0:
        print("Пока нет ни одного рецепта.")
        print("Создайте первый рецепт через пункт 1.")

    else:
        for i in range(len(recipes)):
            recipe = recipes[i]

            print("Рецепт " + str(i + 1) + ": " + recipe.title)
            print_recipe(recipe)
            print()

def scale_recipe(recipes):
    print_result("РАСЧЕТ ПОРЦИЙ")
    print_recipes(recipes)

    if len(recipes) == 0:
        return

    number = int(input("Какой рецепт пересчитать? Введите номер: "))

    if number < 1 or number > len(recipes):
        print("Рецепта с таким номером нет.")

        return

    if len(recipes[number - 1].ingredients) == 0:
        print("В этом рецепте пока нет ингредиентов.")

        return

    ratio = float(input("Во сколько раз изменить порции? "))

    try:
        recipe = recipes[number - 1].scale(ratio)

        print("Пересчитанный рецепт:")
        print_recipe(recipe)

    except ValueError:
        print("Коэффициент должен быть положительным.")

def add_recipe_to_shopping_list(recipes, shopping_list):
    print_result("ДОБАВЛЕНИЕ В ПОКУПКИ")
    print_recipes(recipes)

    if len(recipes) == 0:
        return

    number = int(input("Какой рецепт добавить в покупки? Введите номер: "))

    if number < 1 or number > len(recipes):
        print("Рецепта с таким номером нет.")

        return

    if len(recipes[number - 1].ingredients) == 0:
        print("Нельзя добавить в покупки рецепт без ингредиентов.")

        return

    portions = float(input("На сколько порций покупать продукты? "))

    try:
        shopping_list.add_recipe(recipes[number - 1], portions)
        print("Добавлено в покупки.")

    except ValueError:
        print("Количество порций должно быть положительным.")

def show_shopping_list(shopping_list):
    products = shopping_list.get_list()

    print_result("МОИ ПОКУПКИ")

    if len(products) == 0:
        print("Список покупок пуст.")

    else:
        print("Нужно купить:")

        for ingredient in products:
            print("*", ingredient)

recipes = []
shopping_list = ShoppingList()

while True:
    print()
    print_menu()

    choice = input("Ваш выбор: ")

    if choice == "1":
        create_recipe(recipes)

    elif choice == "2":
        show_all_recipes(recipes)

    elif choice == "3":
        add_ingredient_to_recipe(recipes)

    elif choice == "4":
        scale_recipe(recipes)

    elif choice == "5":
        add_recipe_to_shopping_list(recipes, shopping_list)

    elif choice == "6":
        show_shopping_list(shopping_list)

    elif choice == "0":
        break

    else:
        print("Такого действия нет.")
