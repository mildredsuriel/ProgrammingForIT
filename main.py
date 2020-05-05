# Import os, used for getting Environmental variables
import os
# Import datetime, used for getting the current time
import datetime
# Import time, used to put a thread to sleep
import time
# Import threading, used to create a userInput thread and checkText thread
import threading
# Import re, used for perform regex format checking on phone numbers and time
import re
# Import twilio, used for sending our text messages
from twilio.rest import Client

# Get your account information from the OS environmental variables.
# OS environmental variables are used so that you do not have to enter your private credentials into this program.
# The user of the program will just have to create OS environmental variables for the program to read.
# To set up the OS environmental variables for your account's info, follow this link's instructions:
# https://www.techjunkie.com/environment-variables-windows-10/
# OS environmental variables are needed for the ACCOUNT_SID and AUTH_TOKEN provided on your twilio account page
# Here's my trial account's information. Note: Even if you uncomment out this to use my account, it will only
# allow you to text verified numbers, which are the numbers used in my demo. If you want a number added as
# verified, I will have to have twilio generate a verification code to your number and confirm the code
# account_sid = AC6f53242d6a167d14f8cfd4711258e0ba
# auth_token = 1ae24fc3ba57f5b8b58659f18c763c5b
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
account_sid = os.environ.get('TWILIO_ACCOUNT_SID')


# This is the number assigned to my account on twilio that all of the messages will be sent from
from_number = "205-754-9752"

# Create our client object using the Client function within the twilio library
client = Client(account_sid, auth_token)

# Keep track of whether the user has specified to stop running the program so that we can end the threads
programRunning = 1

# Confirm that user input is correct with a regex comparison
def verifyNumber(phoneNumber):
    # Phone regex used from https://stackoverflow.com/questions/3868753/find-phone-numbers-in-python-script
    # TODO : confirm if all of the numbers that this regex allows through are also supported by twilio's API
    phoneRegex = "(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})"
    if(re.search(phoneRegex,phoneNumber)):
        print("Valid number! (" + phoneNumber + ") \n")
        return 1

    return 0

# Confirm that user input is correct with a regex comparison
# We only allow HH:MM:SS format with a maximum value of 23:59:59
def verifyTime(specifiedTime):
    # Time regex used from https://www.oreilly.com/library/view/regular-expressions-cookbook/9781449327453/ch04s06.html
    timeRegex = "^(2[0-3]|[01]?[0-9]):([0-5]?[0-9]):([0-5]?[0-9])$"
    if(re.search(timeRegex, specifiedTime)):
        return 1

    return 0

# Add an entry to our CSV file to be automatically sent
def addText():
    to_number = input("What phone number would you like to send the text to? : ")

    # Confirm that the number is a valid number, if not exit this function
    if not verifyNumber(to_number):
        print("Error: The phone number is not in a valid format")
        return -1

    message = input("What is the message that you would like to send? NOTE: This message may not contain a comma! : ")
    if "," in message:
        print("Error: The message cannot contain a comma since it is being saved to a CSV file")
        return -1

    interval = input("How often would you like for this text message to be sent (HH:MM:SS format up to 23:59:59) : ")

    # Confirm that the time is in HH:MM:SS format, if not exit this function
    if not verifyTime(interval):
        print("Error: The time is not in HH:MM:SS valid format")
        return -1

    last_time = input("At what time would you like to start sending? NOTE: provide this in minutes : ")

    # Confirm that the time is in HH:MM:SS format, if not exit this function
    if not verifyTime(last_time):
        print("Error: The time is not in HH:MM:SS valid format")
        return -1

    # Take all of the information needed to generate the text and create a comma delimitted string
    csvFormat = ','.join([to_number, message, interval, last_time])

    # Open our csv file to add the new text message
    with open("GeneratedTexts.csv", "a") as file:
        file.write(csvFormat)

def displayTexts():
    i = 0
    with open("GeneratedTexts.csv", "r") as file:
        fileContents = file.readlines()

        for line in fileContents:
            # The information is comma delimited, meaning that we have to split each line of text into the appropriate
            # fields based on commas
            [to_number, message, interval, last_time] = line.rstrip().split(",")

            # Increment
            i += 1

            # Display which text entry this is
            print(str(i) + " : ")
            # Create some spaces at the beginning of the next line for good allignment
            allignment = " " * (len(" : ") + i)
            # Print out each field needed to generate the text message
            print(allignment + "[Recipient : " + to_number + "]")
            print(allignment + "[Message   : " + message + "]")
            print(allignment + "[Interval  : " + interval + "]")
            print(allignment + "[Last Time : " + last_time + "] \n")

# function to send the text using the client object from the twilio API
def sendText(textNumber):
    # If the text number is less than 0, then it is not representing a line in our file to read.
    # Instead, we are trying to send a one time text right now, so get the information to send
    if textNumber < 0:
        # Get the number and message for the text
        to_number = input("What phone number would you like to send the text to? : ")

        # Confirm that the number is a valid number, if not exit this function
        if not verifyNumber(to_number):
            print("Error: The phone number is not in a valid format")
            return -1

        message = input( "What is the message that you would like to send? : ")

        try:
            # Send the text message over the twilio API object
            client.messages.create(from_=from_number, to=to_number, body=message)
        except:
            print("ERROR: The text failed to send for some reason, please try again")

    # We are sending a text from our list either automatically or by choosing to
    else:
        # Open the file that contains all of the text messages that are being generated
        with open("GeneratedTexts.csv", "r") as file:
            # Read in each line into a list
            fileContents = file.readlines()

            # If the number of lines is less than the line number selected, it means the line doesn't exist
            if len(fileContents) < textNumber:
                print("ERROR: You have chosen an entry that does not exist. Use option 1 to see options again.")
            else:
                # Convert each line to their appropriate fields
                [to_number, message, interval, last_time] = fileContents[textNumber].rstrip().split(",")

                try:
                    # Send the text message over the twilio API object
                    client.messages.create(from_=from_number, to=to_number, body=message)
                except:
                    print("ERROR: The text failed to send for some reason, please try again")

# Check to see if any of the texts should be sent
def checkTexts():
    global programRunning
    while programRunning:
        # List to keep track of which texts were sent during this check
        textsSent = []

        # Open the file that contains all of the text messages that are being generated
        with open("GeneratedTexts.csv", "r") as file:
            # Keep track of what line we are looking at
            i = 0
            for line in file:
                # Read in each field from each line
                [to_number, message, interval, last_time] = line.rstrip().split(",")

                # Take the interval field and break it up into hours:minutes:seconds
                [intervalHours, intervalMinutes, intervalSeconds] = interval.split(":")
                # Take the last_time field and break it up into hours:minutes:seconds
                [lastHours, lastMinutes, lastSeconds] = last_time.split(":")

                # Take the interval time and convert it to seconds
                totalIntervalSeconds = (int(intervalHours) * 60 * 60) + (int(intervalMinutes) * 60) + int(intervalSeconds)

                # Take the last_time and convert it to seconds
                totalLastSeconds = (int(lastHours) * 60 * 60) + (int(lastMinutes) * 60) + int(lastSeconds)

                # Take the current time and convert it to seconds
                currentTime = datetime.datetime.now()
                totalCurrentSeconds = (currentTime.hour * 60 * 60) + (currentTime.minute * 60) + currentTime.second

                # If we take the current time and subtract the last time that the text was sent and that time is greater
                # than the interval we are supposed to be sending the text message, then we need to send the text and
                # modify the last_time field for the text that was sent
                if (totalCurrentSeconds - totalLastSeconds > totalIntervalSeconds):
                    sendText(i)
                    # Add the current line number to our list so we know to update the last_time
                    textsSent.append(i)

                # Increment i to indicate that we are done looking at this line in the file
                i += 1

        # If any texts were sent, we need to modify the last time that they were sent
        if len(textsSent) > 0:
            # Read each line number in the list
            for line_number in textsSent:
                # Update the line number's last_time field with the currentTime
                modifyLastTime(line_number, currentTime)

        # Put this function to sleep for 30 seconds so that we are not constantly looping on it
        time.sleep(30)

# Update the last time for a message
def modifyLastTime(textNumber, currentTime):
    # Open the file that contains all of the text messages that are being generated
    with open("GeneratedTexts.csv", "r") as file:
        # Store each line in a variable
        fileContents = file.readlines()

        # Break out each field for the text that we are updating
        [to_number, message, interval, last_time] = fileContents[textNumber].rstrip().split(",")
        # Update the last_time for the text that we are updating to be the current time
        last_time = currentTime.strftime("%H:%M:%S")

        # Update the fileContents variable that represents our entire file
        fileContents[textNumber] = ','.join([to_number, message, interval, last_time])

    # Now we're opening the file to write to it and update it
    with open("GeneratedTexts.csv", "w") as file:
        # Write each line for fileContents back to the file. Make sure we strip \r so we don't end up with extra lines
        for line in fileContents:
            file.write(line.rstrip() + "\n")

# TODO : Make it so that entries can be deleted
def deleteText(textNumber):
    return 1

# TODO : Make it so that entries can be modified
def modifyText(textNumber):
    return 1

def userInput():
    global programRunning
    while programRunning:
        print("Choose one of the following options: \n")
        print("1. Display texts currently being generated \n")
        print("2. Add a new text to be generated \n")
        print("3. Send a one time text now \n")
        print("4. Send one of the saved texts now \n")
        print("5. Delete a text entry (currently unsupported) \n")
        print("6. Modify a text entry (currently unsupported) \n")
        print("7. Quit the program \n")
        userChoice = input()
        if userChoice == "1":
            displayTexts()
        elif userChoice == "2":
            addText()
        elif userChoice == "3":
            # Negative value means a one time text
            sendText(-1)
        elif userChoice == "4":
            displayTexts()
            print("Enter the text entry number that you want to send : ")

            # Attempt to convert the user's input to an int.
            try:
                userChoice = int(input())

                # Text entries are only positive numbers, negative numbers mean its a one time text
                if userChoice > 0 :
                    sendText(userChoice)
                else :
                    print("ERROR: You specified a negative number, which represents a one time text. Try again \n")
            except:
                print("ERROR: Input not recognized as a valid integer. Try again \n")
        elif userChoice == "5" :
            print("Enter the text entry number that you want to delete : ")

            # Attempt to convert the user's input to an int.
            try:
                userChoice = int(input())

                # Text entries are only positive numbers, negative numbers mean its a one time text
                if userChoice > 0 :
                    deleteText(userChoice)
                else :
                    print("ERROR: You specified a negative number, which represents a one time text. Try again \n")
            except:
                print("ERROR: Input not recognized as a valid integer. Try again \n")
        elif userChoice == "6" :
            print("Enter the text entry number that you want to delete : ")

            # Attempt to convert the user's input to an int.
            try:
                userChoice = int(input())

                # Text entries are only positive numbers, negative numbers mean its a one time text
                if userChoice > 0 :
                    modifyText(userChoice)
                else :
                    print("ERROR: You specified a negative number, which represents a one time text. Try again \n")
            except:
                print("ERROR: Input not recognized as a valid integer. Try again \n")
        elif userChoice == "7" :
            programRunning = 0
            print("Program terminated \n")
            return 1
        else:
            print("Invalid option! Choose one of the options provided \n")

if __name__ == "__main__":
    # Create 2 threads, one for the user's input and one for the auto-text sending
    userInputThread  = threading.Thread(target=userInput, args=())
    checkTextsThread = threading.Thread(target=checkTexts, args=())

    # Start our userInput and checkTexts threads
    userInputThread.start()
    checkTextsThread.start()

    # Join the threads together. Since they're both in while True loops, we will never exit this main function
    userInputThread.join()
    checkTextsThread.join()