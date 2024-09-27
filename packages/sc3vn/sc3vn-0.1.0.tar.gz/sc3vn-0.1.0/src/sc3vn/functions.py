#Define variables
prevImage = []



def printImage(image):
    global prevImage
    if (len(image) == 15 or (image == "null")):
        for i in range(0,15):
            #Check if an Image was inputted
            if not (image == "null") :
                #If there was an Image, print it out
                print("[" + image[i] + "]")
            else:
                #Otherwise, print the previous Image if there was one
                if not (not prevImage):              
                    print("[" + prevImage[i] + "]")
                else:
                    print("[                                                            ]")

    #Set the variable prevImage to the most recently printed image
    if (image != "null"):
        prevImage = image

def printText(text, lineAmount="null"):
    #Declare variables
    toPrint = ""
    complete = False
    #Make a list of all words in the text
    words = text.split(" ")
    lines = 0
    
    while not complete:
        #Clear the previous values from buffer
        toPrint = ""

        #Repeat until there are no more words
        while len(words) > 0:
            if (len(toPrint) + len(words[0])) <= 60:
                #If there is space for the next word, add it to the buffer and remove it from the list
                toPrint = toPrint + words[0]
                words.pop(0)
                if (len(toPrint)) < 60:
                    #If there is room for a space, add it to the buffer
                    toPrint = toPrint  + " "
            else:
                #If there isn't space for the next word, check if it is longer than 60 characters to prevent an infinite loop
                if len(words[0]) > 60:
                    print("[Error: Words cannot be longer than 60 characters!           ]")
                    complete = True
                #Exit the loop
                break

        #Exit the loop if there are no more words to add
        if len(words) == 0:
            complete = True

        #Add spaces if neccesary
        if not (len(toPrint) == 60):
            toPrint = toPrint + " " * (60 - len(toPrint))

        #Print the buffer
        print("[" + toPrint + "]")
        lines += 1

    #Print remaining lines if neccesary
    #If the line amount isn't specified:
    if (lineAmount == "null"):
        if lines < 4:
            i = 4 - lines
            while i > 0 :
                i-=1
                print("[                                                            ]")
    #If it is, print the specified amount
    else:
        i = 0
        while (i < lineAmount):
            i += 1
            print("[                                                            ]")


def askQuestion(question, answers, image="null"):
    #Add newlines, 49 so that it doesn't compress automatically
    print("\n" * 49)
    print("[============================================================]")
    #Print Image
    printImage(image)
    print("[============================================================]")
    #Ask Question
    printText(question, 1)
    j = 1
    for i in answers:
        #Print out options
        printText("("+str(j)+"). " + i, 1)
        j = j + 1

    #Add the bar at the bottom
    print("[              Press 1 to " + str(len(answers)) + " to select an option              ]")
    print("[============================================================]")



#Functions above here shouldn't be called, they are just for me :)
#------------------------------------------------------------------------------------------------------------------------

def AskPrompt(question, answers, image="null"):
    #Ask prompt
    askQuestion(question, answers, image)
    #Get input
    choice = input("")
    while not (choice.isnumeric() and int(choice) <= len(answers)):
        choice = input("")
        askQuestion(question, answers, image)
    return choice
        
        

def CreateDialogue(text, image="null") :
        print("\n" * 49)
        print("[============================================================]")
        #Print the Image
        printImage(image)
        print("[============================================================]")
        #Write all the text
        printText(text)
        print("[============================================================]")
        input("")


def MainState(image="null") :
    #Ask 1st Question
    choice = AskPrompt("What would you like to do?", ["Act", "Observe"], image)
    if choice == "1":
        return "1"
        #Returns 1 because you chose option 1
    else:
        #ASk 2nd Question
        choice2 = AskPrompt("How would you like to observe?", ["Look", "Feel"], image)
        match choice2:
            case "1":
                return "2-1"
                #returns "2-1" because you chose option 2(Observe) then 1(Look)
            case "2":
                return "2-2"

