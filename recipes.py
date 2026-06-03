class Ingredient:
    def __init__(self, name, quantity, unit):
        self.name = name
        self.quantity = quantity
        self.unit = unit

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        value = float(value)

        if value <= 0:
            raise ValueError("Количество должно быть положительным")
        
        self._quantity = value

    def __str__(self):
        return f"{self.name}: {self.quantity} {self.unit}"

    def __repr__(self):
        return f"Ingredient('{self.name}', {self.quantity}, '{self.unit}')"

    def __eq__(self, other):
        return self.name == other.name and self.unit == other.unit

class Recipe:
    def __init__(self, title, ingredients=None):
        self.title = title
        self.ingredients = []

        if ingredients is not None:
            for ingredient in ingredients:
                self.add_ingredient(ingredient)

    def add_ingredient(self, ingredient):
        for item in self.ingredients:
            if item == ingredient:
                item.quantity = item.quantity + ingredient.quantity

                return

        self.ingredients.append(ingredient)

    @staticmethod
    def is_valid_ratio(ratio):
        if type(ratio) == int or type(ratio) == float:
            if ratio > 0:
                return True

        return False

    def scale(self, ratio):
        if not Recipe.is_valid_ratio(ratio):
            raise ValueError("Коэффициент должен быть положительным")

        new_recipe = Recipe(self.title)

        for ingredient in self.ingredients:
            new_ingredient = Ingredient(ingredient.name, ingredient.quantity * ratio, ingredient.unit)
            new_recipe.add_ingredient(new_ingredient)

        return new_recipe

    def __len__(self):
        return len(self.ingredients)

    def __str__(self):
        result = self.title + "\n"

        for ingredient in self.ingredients:
            result += str(ingredient) + "\n"

        return result.strip()

class DietaryRecipe(Recipe):
    def __init__(self, title, diet_type, ingredients=None):
        super().__init__(title, ingredients)
        self.diet_type = diet_type

    def scale(self, ratio):
        scaled = super().scale(ratio)
        new_recipe = DietaryRecipe(scaled.title, self.diet_type, scaled.ingredients)

        return new_recipe

    def __str__(self):
        return "[" + self.diet_type + "] " + super().__str__()

class ShoppingList:
    def __init__(self):
        self._items = []

    def add_recipe(self, recipe, portions):
        if not Recipe.is_valid_ratio(portions):
            raise ValueError("Количество порций должно быть положительным")

        scaled = recipe.scale(portions)

        for ingredient in scaled.ingredients:
            self._items.append((ingredient, recipe.title))

    def remove_recipe(self, title):
        items = []

        for ingredient, recipe_title in self._items:
            if recipe_title != title:
                items.append((ingredient, recipe_title))

        self._items = items

    def get_list(self):
        products = {}

        for ingredient, recipe_title in self._items:
            key = (ingredient.name, ingredient.unit)

            if key in products:
                products[key] += ingredient.quantity

            else:
                products[key] = ingredient.quantity

        result = []

        for key in products:
            name, unit = key
            quantity = products[key]
            
            result.append(Ingredient(name, quantity, unit))

        for i in range(len(result)):
            for j in range(len(result) - 1):
                if result[j].name > result[j + 1].name:
                    result[j], result[j + 1] = result[j + 1], result[j]

        return result

    def __add__(self, other):
        new_list = ShoppingList()

        for item in self._items:
            new_list._items.append(item)

        for item in other._items:
            new_list._items.append(item)

        return new_list
