from __future__ import annotations

class Food:

    class Dairy:
        BASE = "/dairy"
        EGG = "/dairy/egg"
        MILK = "/dairy/milk"
        LACTOSE_FREE_MILK = "/dairy/milk/lactose_free"
        YOGURT = "/dairy/yogurt"
        GREEK_YOGURT = "/dairy/yogurt/greek"
        BUTTER = "/dairy/butter"
        SALTED_BUTTER = "/dairy/butter/salted"
        UNSALTED_BUTTER = "/dairy/butter/unsalted"

        class Cheese:
            BASE = "/dairy/cheese"
            CHEESE_STICK = "/dairy/cheese/stick"
            PARMESAN = "/dairy/cheese/parmesan"
            MOZZARELLA = "/dairy/cheese/mozzarella"

        # def __name__(self):
        #     return "/dairy"


    class Meat:
        BASE = "/meat"
        CHICKEN = "/meat/chicken"
        BEEF = "/meat/beef"
        GROUND_BEEF = "/meat/beef/ground"
        STEAK = "/meat/beef/steak"
        PORK = "/meat/pork"
        GROUND_PORK = "/meat/pork/ground"
        HAM = "/meat/pork/ham"
        BACON = "/meat/bacon/pork"
        TURKEY_BACON = "/meat/bacon/turkey"
        SAUSAGE = "/meat/sausage"
        CHICKEN_APPLE_SAUSAGE = "/meat/sausage/chicken_apple"
        FISH = "/meat/fish"
        SALMON = "/meat/fish/salmon"
        SHRIMP = "/meat/shrimp"
        
    class Fruit:
        BASE = "/fruit"
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
        BASE = "/veggie"
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
        BASE = "/bread"
        BREAD = "/bread"
        BAGUETTE = "/bread/baguette"
        BAGEL = "/bread/bagel"

    class Grain:
        BASE = "/grain"
        RICE = "/grain/rice"
        FLOUR = "/grain/flour"

    class Sugar:
        BASE = "/sugar"
        BROWN = "/sugar/brown"
        POWDERED = "/sugar/powdered"
        WHITE = "/sugar/white"

    class Baking:
        BASE = "/baking"
        SODA = "/baking/soda"
        POWDER = "/baking/powder"
        YEAST = "/baking/yeast"

    class Noodle:
        BASE = "/noodle"
        PASTA = "/noodle/pasta"
        RAMEN = "/noodle/ramen"

    class Sauce:
        BASE = "/sauce"
        SOY_SAUCE = "/sauce/soy"
        CANE = "/sauce/cane"
        HANGRY = "/sauce/hangry"

    class Spice:
        BASE = "/spice"
        SALT = "/spice/salt"
        MSG = "/spice/msg"
        GARLIC_POWDER = "/spice/garlic_powder"
        TUMERIC = "/spice/tumeric"

    class Drink:
        BASE = "/drink"
        WATER = "/drink/water"
        SODA = "/drink/soda"

        class Caffeine:
            BASE = "/drink/caffeine"
            MONSTER = "/drink/caffeine/monster"
            ALANI = "/drink/caffeine/alani"
            COFFEE = "/drink/caffeine/coffee"
            
        class Alcohol:
            BASE = "/drink/alcohol"
            VODKA = "/drink/alcohol/vodka"
            
            class Liqueur:
                BASE = "/drink/alcohol"
                KAHLUA = "/drink/alcohol/liqueur/kahlua"
            # LIQUEUR = "/drink/alcohol/liqueur"

            class Malt:
                BASE = "/drink/malt"
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