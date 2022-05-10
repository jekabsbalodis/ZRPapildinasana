from Constants import NO, PROHIBITED_CLASSES, YES, YES_FOR_SOME_SPORTS, YES_WITH_EXCEPTIONS


def stringInput(message):
    userInput = str(input(message))
    return userInput


def prohibited(message, errorMessage):
    userInput = input(message)
    if userInput == YES:
        return userInput
    elif userInput == NO:
        return userInput
    elif userInput == YES_FOR_SOME_SPORTS:
        return userInput
    elif userInput == YES_WITH_EXCEPTIONS:
        return userInput
    else:
        print(errorMessage)
        return prohibited(message, errorMessage)


def prohibitedClass(message, errorMessage):
    userInput = input(message)
    userInputAsList = userInput.split()
    for prClass in userInputAsList:
        if prClass in PROHIBITED_CLASSES:
            return userInput
    if len(userInputAsList) < 1 or len(userInput) < 1:
        print(errorMessage)
        return prohibitedClass(message, errorMessage)


def toInclude(message, errorMessage):
    userInput = input(message)
    if userInput == YES:
        return userInput
    elif userInput == NO:
        return userInput
    else:
        print(errorMessage)
        return toInclude(message, errorMessage)
