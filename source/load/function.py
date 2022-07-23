"""
Defines mathematical functions that are generally used in the game
"""


def largest_divisor_within_interval(num: int, lowest: int = 1, highest: int | None = None, start: int | None = None) -> int:
    """
    Finding largest divisor winthin an interval function, designed specifically for this game
    """
    from math import ceil
    if start is None: start = ceil(num / 2) # if start is not specified
    if highest is None: highest = num - 1 # if highest is not specified

    if start < lowest: raise ValueError("start value is smaller than lowest range")
    if lowest < 1 or highest < 0: raise ValueError("invalid range")

    # the order of checking is reversed (e.g. start -> ...-> 3 -> 2 -> 1)
    for divisor in reversed(range(start+1)):
        if num % divisor == 0 and lowest <= divisor <= highest:
            return divisor

    raise ValueError("n is prime or can't find an appropriate divisor for n")


def lerp(goal: int | float, current: int | float, dt: int = 1):
    """
    Linear interpolation function
    """
    difference = goal - current

    if difference > dt:
        return current + dt
    elif difference < -dt:
        return current - dt

    return goal
