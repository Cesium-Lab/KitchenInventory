from pint import Quantity

def approx_qty(a: Quantity, b: Quantity, bound = 1e-7):
    return abs((a - b).m) < bound