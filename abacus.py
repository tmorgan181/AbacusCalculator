#TRENTON MORGAN
#CS 2200
#HW 1
#09/05/19

#This program simulates the addition of two numbers using an abacus. It takes
#two decimal numbers having up to 12 digits each as inputs, "loads" each onto a
#digital abacus, and prints an ASCII representation of each abacus. The sum
#is then taken by adding the values of each rod on both abacuses, properly
#handling any carry that occurs. The result is then printed as an ASCII abacus.

#UTILITY FUNCTIONS#
#-----------------#

#Print abacus row-by-row (NOT rod-by-rod) with a bar separating the top and
#bottom beads.
def printAbacus(abacus):
    #Print top beads first
    for i in range(0, 2):
        for j in range(NUM_RODS):
            print(abacus[j][i], end = ' ')
        print('\n')

    #Break line
    print("-------------------------")

    #Print bottom beads last
    for i in range(2, NUM_BEADS + 2):
        for j in range(NUM_RODS):
            print(abacus[j][i], end = ' ')
        print('\n')

    return

#Load an individual rod on the digital abacus with value rodVal.
def loadRod(abacus, rod, rodVal):
    #To represent the value on the rod, determine where the spaces should be,
    #then fill in the rest of the column with beads ('o's)
    if rodVal >= 5:
        space1 = 0      #space1 on index 0, indicating a top bead is used
        rodVal -= 5     #Reduce rodVal to be used in finding space2
    else:
        space1 = 1      #space1 on index 1, indicating no top bead is used

    space2 = rodVal + 2 #space2 is selected based on the remaining rodVal

    #After determining where the spaces will be, we modify the current rod's
    #list to reflect its value
    for j in range(0, NUM_BEADS + 2):
        if j == space1 or j == space2:
            abacus[rod - 1][j] = ' '
        else:
            abacus[rod - 1][j] = 'o'
            
    return

#Load an input onto the abacus rod-by-rod starting at the right end (highest
#index). We convert the input's decimal digit value into the proper
#configuration of beads on the rod.
def loadAbacus(abacus, num):
    inputLen = len(num)     #Number of digits in input, useful for extracting
                            #the value of each one.

    #Each rod is configured one-by-one in this for loop
    for i in range(NUM_RODS):
        rod = NUM_RODS - i      #Allows right-to-left indexing of the abacus,
                                #i.e. first iteration i = 0, rod = 13

        #For all rods beyond the number of digits in the input, rodVal is 0. All
        #other values are taken from the corresponding digit of the input num.
        if i >= inputLen:
            rodVal = 0
            #print(rodVal)
        else:
            rodVal = int(num[(inputLen - i) - 1])

        #Double check rodVal is valid ( <= 9 and > 0)
        if rodVal > 10 or rodVal < 0:
            return "ERROR: rodVal is invalid"

        #With valid rodVal, configure the current rod
        loadRod(abacus, rod, rodVal)

    return

#Convert a rod (list of beads and spaces) into its decimal equivalent. This is
#the reverse of the process used in "loading" the rods.
def value(rod):
    rodVal = 0

    if rod[0] == ' ':       #Space at index 0 denotes a 5-value bead is used
        rodVal += 5

    rodVal += rod[2:].index(' ')    #The remainder of the value is given by the
                                    #index of the second space on the rod

    return rodVal



#DRIVER FUNCTION#
#---------------#

#First we take in the two addends as input, checking that each is valid and
#requesting a new input if invalid. The numbers are taken in as a string so as
#to easily manipulate the individual digits.
validInput = False
while (not validInput):
    num1 = input("Please enter the first number: ")

    #An input is invalid if it contains > 12 digits, any digit is not a number,
    #or the number is negative. This if statement checks that all three
    #conditions are met for valid input and informs the user of an error if the
    #input is invalid.
    if (len(num1) > 12) or (not num1.isdigit()) or (int(num1) < 0):
        print("That is an invalid input. Please try again.")
    else:
        validInput = True

#We repeat the process for the second input.
validInput = False
while (not validInput):
    num2 = input("Please enter the second number: ")

    if (len(num2) > 12) or (not num2.isdigit()) or (int(num2) < 0):
        print("That is an invalid input. Please try again.")
    else:
        validInput = True

print('\n')

#After receiving two valid inputs, we are ready to map them onto our digital
#abacus. The abacus is represented as a list of lists with dimensions NUM_RODS
#columns and NUM_BEADS + 2 positions per rod (the +2 is for spaces). This
#program is based on the Japanese-style abacus, which leaves out the excess
#beads that are present on the Chinese-style.
NUM_RODS = 13
NUM_BEADS = 5

#Abacus is created with the specified dimensions, defaulting to 'k' in every
#position so it is easy to tell if the abacus failed to load correctly
abacus1 = [['k' for x in range(NUM_BEADS + 2)] for y in range(NUM_RODS)]
loadAbacus(abacus1, num1)        #Load the first input onto first abacus
print(num1, "on an abacus is:")
printAbacus(abacus1)

#Repeat for second input
abacus2 = [['k' for x in range(NUM_BEADS + 2)] for y in range(NUM_RODS)]
loadAbacus(abacus2, num2)       #Load the second input onto second abacus
print(num2, "on an abacus is:")
printAbacus(abacus2)

#With both addends loaded onto abacuses, we are ready to perform the addition.
#This is done rod-by-rod, right-to-left, taking the sum of each pair of rods and
#representing it on a seperate sum abacus. When a pair's sum exceeds 10, the
#boolean variable carry becomes True, adding 1 to the next sum.
sumAbacus = [['k' for x in range(NUM_BEADS + 2)] for y in range(NUM_RODS)]
decimalSum = int(num1) + int(num2)        #Used only to verify abacus sum

carry = False
for i in range(NUM_RODS):
    rod = NUM_RODS - i  #Index the rods right-to-left (column 13 first)

    #Find the sum of the two rods
    rodSum = value(abacus1[rod - 1]) + value(abacus2[rod - 1])

    if carry:           #If a carry is necessary, add 1 to the sum
        rodSum += 1
        
    if rodSum >= 10:    #If the sum is >= 10, we must carry 1 on the next rod
        carry = True
        rodSum -= 10    #Taking out the carry reduces the sum by 10
    else:
        carry = False   #Sum < 10, carry is unnecessary

    #After the sum of the two rods is calculated, load it onto the corresponding
    #rod of the sumAbacus
    loadRod(sumAbacus, rod, rodSum)

#Finally, print the resulting sum abacus
print("The sum of", num1, "and", num2, "is", decimalSum, ". On an abacus:")
printAbacus(sumAbacus)





