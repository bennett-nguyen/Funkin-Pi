"""
Defines mathematical functions that are generally used in the game
"""
def largest_divisor(num: int, lowest_range: int = 1, highest_range: int | None = None, start: int | None = None) -> int:
    """
    Finding largest divisor function, designed specifically for this game
    """
    from math import ceil
    if start is None: start = ceil(num / 2)
    if highest_range is None: highest_range = num - 1

    if start < lowest_range: raise ValueError("start value is smaller than lowest range")
    if lowest_range < 1 or highest_range < 0: raise ValueError("invalid range")

    for divisor in reversed(range(start+1)):
        if num % divisor == 0 and lowest_range <= divisor <= highest_range:
            return divisor

    raise ValueError("n is prime or can't find an appropriate divisor for n")


def lerp(goal, current, dt=1):
    """
    Linear interpolation function
    """
    difference = goal - current

    if difference > dt:
        return current + dt
    elif difference < -dt:
        return current - dt

    return goal

