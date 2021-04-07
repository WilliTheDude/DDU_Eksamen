import speech_recognition as sr  # makes sure that Bagley can understand what you're saying
import pyttsx3  # Enables text to speech so that Bagley can respond on your commands
import datetime  # Enables Bagley to get the real time and date
import wikipedia  # allows the program to search wikipedia for information's
from phue import Bridge  # This library allow us to connect to a philips hue bridge
import pytz  # Enables us to define time zones
import json  # This enables us to work with json files
import webbrowser  # This enables us to open a web-browser in google
from googlesearch import search  # Enables us to search google
import time  # Enables to set at timer for a quick break
from word2number import w2n  # allows us to converte text numbers to numberes


""" \_(*>*)_/ WilliTheDude"""
# Initialize the pyttsx3 library
engine = pyttsx3.init()
voices = engine.getProperty('voices')  # gets the voices for Bagley

# Bagley's voice
for voice in voices:
    # print(voice)  # prints all the voice to the terminal
    if voice.languages[0] == 'en_GB':
        engine.setProperty('voice', voice.id)
        break

rate = engine.getProperty('rate')
engine.setProperty('rate', 180)

volume = engine.getProperty('volume')
engine.setProperty('volume', 0.1)


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
        recognition.adjust_for_ambient_noise(source)
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


"""
# This section controls the light
b = Bridge('192.168.0.205')
b.connect()
b.get_api()
"""
"""
def turnLightsOnAndOffControls(userLightCommand):
    with open('Data/LightControls.json', 'r') as lc:
        light_command = json.load(lc)

        # Turn lights on, commands
        for lightsOn in light_command['TurnOnLights']:
            if lightsOn['command'].lower() in userLightCommand:
                b.set_group(1, 'on', True)

        # Turn lights off, commands
        for lightsOff in light_command['TurnOffLights']:
            if lightsOff['command'].lower() in userLightCommand:
                b.set_group(1, 'on', False)

        # Turn on the firs light, command
        for firstLightOn in light_command['LightBulbOn1']:
            if firstLightOn['command'].lower() in userLightCommand:
                b.set_light(1, 'on', True)

        # Turn off the first light, command
        for firstLightOff in light_command['LightBulbOff1']:
            if firstLightOff['command'].lower() in userLightCommand:
                b.set_light(1, 'on', False)

        # Turn on the second light, command
        for secondLightOn in light_command['LightBulbOn2']:
            if secondLightOn['command'].lower() in userLightCommand:
                b.set_light(2, 'on', True)

        # Turn off the second light, command:
        for secondLightOff in light_command['LightBulbOff2']:
            if secondLightOff['command'].lower() in userLightCommand:
                b.set_light(2, 'on', False)

        # Turn on the third light, command
        for thirdLightOn in light_command['LightBulbOn3']:
            if thirdLightOn['command'].lower() in userLightCommand:
                b.set_light(3, 'on', True)

        # Turn off teh third light, command
        for thirdLightOff in light_command['LightBulbOff3']:
            if thirdLightOff['command'].lower() in userLightCommand:
                b.set_light(3, 'on', False)

        # Turn on the fourth light, command
        for fourthLighton in light_command['LightBulbOn4']:
            if fourthLighton['command'].lower() in userLightCommand:
                b.set_light(4, 'on', True)

        # Turn of the fourth light, command
        for fourthLightOff in light_command['LightBulbOff4']:
            if fourthLightOff['command'].lower() in userLightCommand:
                b.set_light(4, 'on', False)
"""

"""def changeColourOnLight:"""


# This function tells the time
def world_and_local_time(userInputTime):
    # Time for Europe
    with open("Data/TimeZones.json", 'r') as j:
        time_zone = json.load(j)

        # Gives the local time
        for local_time in time_zone['Time']:
            for time_eu in time_zone['Europe']:
                if time_eu['name'].lower() in userInputTime:
                    print("true")
                    break
            else:
                for time_america in time_zone['America']:
                    if time_america['name'].lower() in userInputTime:
                        print("true")
                        break
                else:
                    for time_asia in time_zone['Asia']:
                        if time_asia['name'].lower() in userInputTime:
                            print("true")
                            break
                    else:
                        if local_time['keyword'].lower() in userInputTime:
                            current_time = datetime.datetime.now().strftime("%H:%M")
                            print(f"The time is /{current_time}")
                            speak(f"The time is/{current_time}")
                        break

        # Gives the time for countries in EU
        for countries_eu in time_zone['Europe']:
            if countries_eu['keyword'].lower() in userInputTime and countries_eu['name'].lower() in userInputTime:
                country_capital = countries_eu['capital']
                time_string = "Europe/" + country_capital
                country_time = pytz.timezone(time_string)
                current_time = datetime.datetime.now(country_time).strftime("%H:%M")
                speak(f"in/{country_capital}, " + f"/{countries_eu['name']}, " + f"it's /{current_time}")

        # Gives the time fo countries / stats in America
        for countries_america in time_zone['America']:
            if countries_america['keyword'].lower() in userInputTime and countries_america['name'].lower() in userInputTime:
                america_capital = countries_america['name']
                america_time_string = "America/" + america_capital
                america_country_time = pytz.timezone(america_time_string)
                america_time = datetime.datetime.now(america_country_time)
                speak(f"in/{america_capital}," + "America," + f"the time is/{america_time}")

        # Gives the time for the countries in Asia
        for countries_asia in time_zone['Asia']:
            if countries_asia['keyword'].lower() in userInputTime and countries_asia['name'].lower() in userInputTime:
                asia_capital = countries_asia['capital']
                asia_time_string = "Asia/" + asia_capital
                asia_capital_time = pytz.timezone(asia_time_string)
                asia_time = datetime.datetime.now(asia_capital_time)
                speak(f"in/{asia_capital}," + f"/{countries_asia['name']}," + f"the time is /{asia_time}")


# This function will enable the user to search the wikipedia for answers
def searchWikipedia(userWikipediaStatement):
    if 'wikipedia' in userWikipediaStatement.lower():
        speak("Searching Wikipedia...")
        userWikipediaStatement = userWikipediaStatement.replace("wikipedia", "")
        result = wikipedia.summary(userWikipediaStatement, sentences=4)
        speak("According to wikipedia")
        print(result)
        speak(result)


"""
# This function will allow the user to search google for things by asking the voice assistant a question
def searchGoogleForAnswers(userGoogleInput):
"""

"""
This function allows the user to open a webpage that the voice assistant knows
If the voice assistant doesn't know the webpage it will search google for a result
The voice assistant can open: 1: Google chrome 2: Youtube 3: Netflix  4: Viaplay 5: HBO 6: Gmail 7: Outlook 8: Yahoo mail
"""
def openWebpages(userWebpageInput):
    with open("Data/KnownWebpages.json") as known_webpages:
        webpage_names = json.load(known_webpages)

        # Checks if a known webpage is in the JSON-file
        for webpage in webpage_names['Webpages']:
            if webpage['name'].lower() in userWebpageInput:
                webpage_name = webpage['name']
                the_seeking_page = str(" ")

                if "google" in webpage['name'].lower():
                    the_seeking_page = 'https://www.google.com/'

                elif "gmail" in webpage['name'].lower():
                    the_seeking_page = 'https://mail.google.com/'

                elif "Yahoo mail" in webpage['name'].lower():
                    the_seeking_page = 'https://mail.yahoo.com/'

                elif "outlook" in webpage['name'].lower():
                    the_seeking_page = 'https://outlook.live.com/'

                elif "youtube" in webpage['name'].lower():
                    the_seeking_page = 'https://www.youtube.com/'

                elif "netflix" in webpage['name'].lower():
                    the_seeking_page = 'https://www.netflix.com/'

                elif "viaplay" in webpage['name'].lower():
                    the_seeking_page = 'https://viaplay.com/'

                elif "hbo" in webpage['name'].lower():
                    the_seeking_page = 'https://dk.hbonordic.com/'

                webbrowser.open_new_tab(the_seeking_page)
                print(f"opening/{the_seeking_page}")
                speak(f"Okay, opening/{webpage_name}")
            break

        for webpage in webpage_names['Webpages']:
            # Checks if open appears in the function parameter and checks if the if a known webpage appears
            if ("open" in userWebpageInput) and not(webpage['name'].lower() in userWebpageInput):
                speak("The webpage you are looking for don't exist in my list")
                speak("But this is what i found on google")

                search_text = userWebpageInput[userWebpageInput.index('open') + len('open') + 1]
                result_list = search(query=search_text, tld="co.in", lang="en", num=2, start=0, stop=2, pause=2.0)

                for result in result_list:
                    print(result)


# Setting a timer
def countdown(t):
    while t:
        hours, reminder = divmod(t, 3600)
        mins, secs = divmod(reminder, 60)
        time_formatter= "{:02d}:{:02d}:{:02d}".format(hours, mins, secs)
        print(time_formatter, end="\r")
        time.sleep(1)
        t -= 1
    speak("It is timeeeeeee!")

def timer(userTimerInput):
    duration = [int(i) for i in userTimerInput.split() if i.isdigit()]  # Looking for numbers in the
    print(duration)

    # Checks for seconds
    if 'second' in userTimerInput or 'seconds' in userTimerInput:
        preferred_time = int(duration[0])  # Sets the time in seconds
        print("true")
        countdown(preferred_time)  # Calls the countdown function

    # Checks for minuts
    if 'minute' in userTimerInput or 'minutes' in userTimerInput:
        preferred_time = int(duration[0] * 60)
        print("true")
        countdown(preferred_time)  # Calls the countdown function

    # Checks for hours
    if 'hour' in userTimerInput or 'hours' in userTimerInput:
        preferred_time = int(duration[0] * 3600)
        print("true")
        countdown(preferred_time)  # Calls the countdown function

    try:
        if 'set' and 'timer' and ('hour' or 'hours') in userTimerInput:
            preferred_time = w2n.word_to_num(userTimerInput) * 3600
            print("true")
            countdown(preferred_time)

        if 'set' and 'timer' and ('minute' or 'minutes') in userTimerInput:
            preferred_time = w2n.word_to_num(userTimerInput) * 60
            print("true")
            countdown(preferred_time)

        if 'set' and 'timer' and ('second' or 'seconds') in userTimerInput:
            preferred_time = w2n.word_to_num(userTimerInput)
            print("true")
            countdown(preferred_time)
    except ValueError as e:
        return

# The things Bagley shall do on start up
print("Loading your personal assistant Bagley")
greetUser()

# Checks if the name of the file equals the main file.
# Main
if __name__ == '__main__':

    while True:
        statement = takeCommand().lower()  # Allows Bagley to hear what you're saying
        shutDownBagley = False

        # Checks if the statement variable is empty, if empty Bagley just continues listening
        if statement == 0:
            continue

        # goodbye respond
        # Opens the text fill containing all the goodbye responses
        with open('Data/goodByeSayings.txt', 'r') as goodBye:
            lines = goodBye.readlines()  # Stores the responses in a list

            # loops though every line in the document
            for line in lines:
                # Checks if the what you say matches with one of the lines in the document
                if statement in line:
                    speak("Goodbye, see you later")
                    print("Goodbye, see you later")
                    shutDownBagley = True
                    break

            # Turns of Bagley
            if shutDownBagley:
                break

        # Light controls
        # turnLightsOnAndOffControls(statement)

        # Give the time
        world_and_local_time(statement)

        # Searching wikipedia for questions
        searchWikipedia(statement)

        # Open a webpage
        openWebpages(statement)

        # Set timer
        timer(statement)

        # news

        # search google

        # Forecasting the weather

        # Math



