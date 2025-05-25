from pint import Quantity

def approx_qty(a: Quantity, b: Quantity, bound = 1e-7):
    return abs((a - b).m) < bound

def is_mass(x: Quantity):
    return x.dimensionality == "[mass]"

def is_volume(x: Quantity):
    return x.dimensionality == "[length] ** 3"

def is_density(x: Quantity):
    return x.dimensionality == "[mass] / [length] ** 3"