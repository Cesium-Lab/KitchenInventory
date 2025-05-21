from __future__ import annotations

class Food:

    class Dairy:
        EGG = "/dairy/egg"
        MILK = "/dairy/milk"
        LACTOSE_FREE_MILK = "/dairy/milk/lactose_free"
        YOGURT = "/dairy/yogurt"
        GREEK_YOGURT = "/dairy/yogurt/greek"
        BUTTER = "/dairy/butter"
        SALTED_BUTTER = "/dairy/butter/salted"
        UNSALTED_BUTTER = "/dairy/butter/unsalted"

        class Cheese:
            CHEESE = "/dairy/cheese"
            CHEESE_STICK = "/dairy/cheese/stick"
            PARMESAN = "/dairy/cheese/parmesan"
            MOZZARELLA = "/dairy/cheese/mozzarella"


    class Protein:
        CHICKEN = "/protein/chicken"
        BEEF = "/protein/beef"
        GROUND_BEEF = "/protein/beef/ground"
        STEAK = "/protein/beef/steak"
        PORK = "/protein/pork"
        GROUND_PORK = "/protein/pork/ground"
        HAM = "/protein/pork/ham"
        BACON = "/protein/bacon/pork"
        TURKEY_BACON = "/protein/bacon/turkey"
        SAUSAGE = "/protein/sausage"
        CHICKEN_APPLE_SAUSAGE = "/protein/sausage/chicken_apple"

        class Seafood:
            FISH = "/protein/fish"
            SALMON = "/protein/fish/salmon"
            SHRIMP = "/protein/shrimp"
        
    class Fruit:
        BERRY = "/fruit/berry"
        RASPBERRY = "/fruit/berry/raspberry"
        BLUEBERRY = "/fruit/berry/raspberry"
        BLACKBERRY = "/fruit/berry/raspberry"
        STRAWBERRY = "/fruit/berry/raspberry"
        CHERRY = "/fruit/berry/cherry"
        BANANA = "/fruit/banana"
        APPLE = "/fruit/apple"
        CITRUS = "/fruit/citrus"
        LEMON = "/fruit/citrus/lemon"
        LIME = "/fruit/citrus/lime"
        ORANGE = "/fruit/citrus/orange"
        GRAPE = "/fruit/grape"
        WATERMELON = "/fruit/watermelon"
        PINEAPPLE = "/fruit/pineapple"
        PEACH = "/fruit/peach"
        
    class Vegetable:
        CORN = "/veggie/corn"
        PEAS = "/veggie/peas"
        POTATO = "/veggie/potato"
        PARSEY = "/veggie/parsley"
        BASIL = "/veggie/basil"
        GARLIC = "/veggie/garlic"
        GARLIC_MINCED = "/veggie/garlic/minced"
        PEPPER = "/veggie/pepper"
        TOMATO = "/veggie/tomato"
        ONION = "/veggie/onion"

    class Bread:
        BREAD = "/bread"
        BAGUETTE = "/bread/baguette"
        BAGEL = "/bread/bagel"

    class Grain:
        RICE = "/grain/rice"
        FLOUR = "/grain/flour"

    class Sugar:
        SUGAR = "/sugar"
        BROWN = "/sugar/brown"
        POWDERED = "/sugar/powdered"
        WHITE = "/sugar/white"

    class Baking:
        SODA = "/baking/soda"
        POWDER = "/baking/powder"
        YEAST = "/baking/yeast"

    class Noodle:
        PASTA = "/noodle/pasta"
        RAMEN = "/noodle/ramen"

    class Sauce:
        SOY_SAUCE = "/sauce/soy"
        CANE = "/sauce/cane"
        HANGRY = "/sauce/hangry"

    class Spice:
        SALT = "/spice/salt"
        MSG = "/spice/msg"
        GARLIC_POWDER = "/spice/garlic_powder"
        TUMERIC = "/spice/tumeric"

    class Drink:
        WATER = "/drink/water"
        SODA = "/drink/soda"
        class Caffeine:
            MONSTER = "/drink/caffeine/monster"
            ALANI = "/drink/caffeine/alani"
            COFFEE = "/drink/caffeine/coffee"
            
        class Alcohol:
            VODKA = "/drink/alcohol/vodka"
            
            class Liqueur:
                KAHLUA = "/drink/alcohol/liqueur/kahlua"
            LIQUEUR = "/drink/alcohol/liqueur"

            class Malt:
                MTN_DEW = "/drink/malt/mtn_dew"

def foods():

    def foods_helper(cls: type) -> list[str]:
        constants: list[str] = []
        for name, value in cls.__dict__.items():
            
            if name.isupper() and type(value) is str and value.startswith("/"):
                constants.append(value)
            elif type(value) is type:
                rslt = foods_helper(value)
                for i in rslt:
                    constants.append(i)
        return constants
    return foods_helper(Food)

# if __name__ == "__main__":
#     from pprint import pprint
#     pprint([i for i in foods() if "/drink/alcohol" in i])