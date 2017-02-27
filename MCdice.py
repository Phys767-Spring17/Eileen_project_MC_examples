import random
import matplotlib
import matplotlib.pyplot as plt

import time
import smallcodes as sc

# Globally define some variables to be used with multiple bettor strategies
samplesize = 1000  # How many individual trials
startingFunds = 10000
wagerSize = 100
wagerCount = 10000  # Length of individual trial


def rollDice():
    """
    Function to represent rolling the dice. House wins if roll 100 or 1-50. You win if roll between 51 and 99.
    """

    roll = random.randint(1, 100)

    if roll == 100:
        return False
    elif roll <= 50:
        return False
    elif 100 > roll > 50:
        return True


def dbl_bettor(funds, inital_wager, wager_count, color):
    """
    Making a more complicated bettor (Martingale Strategy). Double your wager when you lose and go back to original
    wager when you win again.
    """

    global dbl_busts  # Adding to see which method make more money/loses more
    global dbl_profits
    value = funds
    wager = inital_wager
    wX = []
    vY = []
    currentWager = 1
    previousWager = 'win'  # We are betting on the previous outcome. Assume start with a win.
    previousWagerAmount = inital_wager

    while currentWager <= wager_count:
        if previousWager == 'win':
            if rollDice():  # rollDice returned True
                value += wager
                wX.append(currentWager)
                vY.append(value)
            else:  # rollDice returned False
                value -= wager
                previousWager = 'loss'
                previousWagerAmount = wager
                wX.append(currentWager)
                vY.append(value)
                if value <= 0:
                    dbl_busts += 1
                    break
        elif previousWager == 'loss':
            # print('We lost last one, so we will be smart and dbl!')
            if rollDice():
                wager = previousWagerAmount * 2

                if (value - wager) < 0:
                    wager = value

                value += wager
                wager = inital_wager
                previousWager = 'win'
                wX.append(currentWager)
                vY.append(value)
            else:
                wager = previousWagerAmount * 2
                # print('We lost', wager)
                if (value - wager) < 0:  # Making it so we bet all that was left. Can't go negative.
                    wager = value
                value -= wager
                previousWager = 'loss'
                previousWagerAmount = wager
                wX.append(currentWager)
                vY.append(value)
                if value <= 0:
                    # print('We broke. Went broke after',currentWager,'bets')
                    dbl_busts += 1
                    break

        currentWager += 1

    # print(value)
    plt.plot(wX, vY, color)
    if value > funds:
        dbl_profits += 1


'''
Adding some more statistics to track losses v wins
xx = 0
broke_count = 0

while xx < 10:
    dbl_bettor(10000,100,1000)
    xx += 1

print('death rate:',(broke_count/float(xx)) * 100)
print('survival rate',100 - ((broke_count/float(xx)) * 100))

#dbl_bettor(10000,100,100)
plt.title('Double Up Results')
plt.xlabel('bets')
plt.ylabel('amount')
plt.axhline(0, color = 'r')
plt.show()
sc.stop() #stops code from here on out. Not interactive like IDL.

#time.sleep(555) #pauses code for set amount of seconds.
'''


def simple_bettor(funds, initial_wager, wager_count, color):
    """
    Simple Bettor, betting the same amount each time. The while loop rolls the dice wager_count times and adds or subtracts
    from the bettor's funds.
    """

    global simple_busts
    global simple_profits
    value = funds
    wager = initial_wager
    wX = []  # wager X
    vY = []  # value y
    currentWager = 1  # wager count starting at one

    while currentWager <= wager_count:  # Run while currentWager is less than wagerCount (defined with global variables)
        if rollDice():
            value += wager  # If you win, add to funds
            wX.append(currentWager)
            vY.append(value)
            # print(value)
        else:
            value -= wager  # lose subtract bet from funds
            wX.append(currentWager)
            vY.append(value)
            # print(value)

            if value <= 0:
                simple_busts += 1
                break


        currentWager += 1

    plt.plot(wX, vY, color)
    if value > funds:
        simple_profits += 1

'''
Giving it a go for simple_bettor. Roll the dice wager_count times (third entry). Being in the while loop says to show me
the results for 100 trials.

x = 0
broke_count = 0

while x < 1000:
    simple_bettor(10000, 100, 1000)
    x += 1
print(('death rate:', (broke_count/float(x)) * 100))
print(('survival rate:', 100 -(broke_count/float(x)) * 100))
plt.axhline(0,color = 'r')
plt.ylabel("Account Value")
plt.xlabel('Wager Count')
plt.title('MC Dice: 100 trials of length 1000')
plt.show()
'''


'''Now run with both bettors to compare which is better.'''
x = 0

simple_busts = 0.0
dbl_busts = 0.0
simple_profits = 0.0
dbl_profits = 0.0

while x < samplesize:
    simple_bettor(startingFunds, wagerSize, wagerCount, 'k')  # K is black for matplotlib
    #simple_bettor(startingFunds, wagerSize * 2, wagerCount, 'g')
    dbl_bettor(startingFunds, wagerSize,wagerCount, 'b')
    x += 1


print(('Simple Bettor Bust Chances:'), (simple_busts/samplesize)*100.00)
print(('Double Bettor Bust Chances:'), (dbl_busts/samplesize)*100.00)
print(('Simple Bettor Profit Chances:'), (simple_profits/samplesize)*100.00)
print(('Double Bettor Profit Chances:'), (dbl_profits/samplesize)*100.00)

plt.axhline(0, color='r')
plt.ylabel('Account value')
plt.xlabel('Wager Count')
plt.show()
