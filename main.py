import speech_recognition as sr  # makes sure that Bagley can understand what you're saying
import pyttsx3  # Enables text to speech so that Bagley can respond on your commands
import datetime  # Enables Bagley to get the real time and date
import wikipedia  # allows the program to search wikipedia for information's
import time  # Enables to set at timer for a quick break
import random

# Initialize the pyttsx3 library
engine = pyttsx3.init()
voices = engine.getProperty('voices')  # gets the voices for Bagley

# Bagley's voice
for voice in voices:
    print(voice)  # prints all the voice to the terminal
    if voice.languages[0] == 'en_GB':
        engine.setProperty('voice', voice.id)
        break


# This function enables Bagley to speak
def speak(text):
    engine.say(text)
    engine.runAndWait()


# This function allows Bagley to greet the user
def greetUser():
    hour = datetime.datetime.now().hour  # gets the current hour

    # This if statements checks the time and gives a shutting response
    if 0 <= hour < 10:
        print("Good morning, did you sleep well?\n Hello, how may i help you")
        speak("Good morning, did you sleep well?")
        speak("Hello, how may i help you")

    elif 10 <= hour < 12:
        print("Good morning\n Hello, how may i help you")
        speak("Good morning")
        speak("Hello, how may i help you")

    elif 12 <= hour < 18:
        print("Good afternoon\n Hello, how may i help you")
        speak("Good afternoon")
        speak("Hello, how may i help you")

    else:
        print("Good evening\n Hello, how may i help you")
        speak("Good evening")
        speak("Hello, how may i help you")


# This function enables Bagley to take commands
def takeCommand():
    recognition = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening....")
        audio = recognition.listen(source)  # uses the function listen from speech_recognition library

    # this try function will help Bagley understand what the user are saying
    try:
        statement = recognition.recognize_google(audio, language='en_GB')
        print(f"{statement}\n")

    # This exception will prevent run time errors
    except Exception as e:
        speak("Pardon me, can you please say that again?")
        return "None"
    return statement


# The things Bagley shall do on start up
print("Loading your personal assistant Bagley")
greetUser()

# Checks if the name of the file equals the main file.
if __name__ == '__main__':

    while True:
        statement = takeCommand().lower()  # Allows Bagley to hear what you're saying
        shutDownBagley = False

        # Checks if the statement variable is empty, if empty Bagley just continues listening
        if statement == 0:
            continue

        # goodbye respond
        # Opens the text fill containing all the goodbye responses
        with open('Data/goodByeSayings.txt') as goodBye:
            lines = goodBye.readlines() # Stores the responses in a list

            # loops though every line in the document
            for line in lines:
                # Checks if the what you say matches with one of the lines in the document
                if line.find(statement):
                    speak("Goodbye, see you later")
                    print("Goodbye, see you later")
                    shutDownBagley = True
                    break

            # Turns of Bagley
            if shutDownBagley:
                break
