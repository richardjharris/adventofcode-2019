import math
inputs = open('q1_input', 'r').readlines()

def fuelCalc(value):
    return int(math.floor(int(value) / 3) - 2)

def recursiveFuelCalc(value):
    total = 0
    while True:
        value = fuelCalc(value)
        if value < 0:
            break
        total += value
    return total

""" calculate fuel by mass/3 (rounded down) - 2, for all modules """
def part1():
    totalFuel = 0
    for mass in inputs:
        fuel = fuelCalc(mass)
        totalFuel += fuel
    print(totalFuel)

""" same as above, but recurse on the result until we get 0 or negative """
def part2():
    totalFuel = 0
    for mass in inputs:
        totalFuel += recursiveFuelCalc(mass)
    print(totalFuel)

part2()
