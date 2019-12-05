inputRange = xrange(145852, 616942 + 1)

"""
input is:
 - 6-digit number
 - within inputRange
 - two adjacent digits are the same
 - digits never decrease
"""

def matchesCriteria(number):
    """ checks rules 3 and 4 on number. assumes rules 1+2 met """
    twoAdjacent = False
    lastDigit = None
    for digit in str(number):
        if lastDigit is None:
            pass
        else:
            if int(lastDigit) > int(digit):
                return False
            elif int(lastDigit) == int(digit):
                twoAdjacent = True
        lastDigit = digit

    if not twoAdjacent:
        return False

    return True

def matchesCriteria2(number):
    """ modified version which does not allow a group of 3+ digits """
    currentChainLength = 0
    twoAdjacentFound = False
    lastDigit = None
    for digit in str(number):
        if lastDigit is None:
            pass
        else:
            if int(lastDigit) > int(digit):
                return False
            elif int(lastDigit) == int(digit):
                currentChainLength += 1
            else:
                if currentChainLength == 1:
                    twoAdjacentFound = True
                currentChainLength = 0
        lastDigit = digit

    if currentChainLength == 1:
        twoAdjacentFound = True

    if not twoAdjacentFound:
        return False

    return True

# let's try again but faster
def findMatchingNumbers(start, end):
    # Go over prefix?


# Quick tests
#print matchesCriteria(111111)  # true
#print matchesCriteria(223450)  # false (decreasing pair 50)
#print matchesCriteria(123789)  # false (no double)

print matchesCriteria2(112233)  # true
print matchesCriteria2(123444)  # false (triplet)
print matchesCriteria2(111122)  # true (four 1s, but double also)

#print len(filter(matchesCriteria, inputRange))
print len(filter(matchesCriteria2, inputRange))
