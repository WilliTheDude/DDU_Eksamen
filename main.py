import os
import wave
import pyaudio
import requests
import speech_recognition as sr  # makes sure that Jarvis can understand what you're saying
import pyttsx3  # Enables text to speech so that Jarvis can respond on your commands
import datetime  # Enables Jarvis to get the real time and date
import wikipedia  # allows the program to search wikipedia for information's
import wolframalpha
from phue import Bridge  # This library allow us to connect to a philips hue bridge
import pytz  # Enables us to define time zones
import json  # This enables us to work with json files
import webbrowser  # This enables us to open a web-browser in google
from googlesearch import search  # Enables us to search google
import time  # Enables to set at timer for a quick break


class AudioFile:
    chunk = 1024

    def __init__(self, audio_file_name):
        """ Init audio stream """
        self.wf = wave.open(audio_file_name, 'rb')
        self.file_name = audio_file_name

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=self.p.get_format_from_width(self.wf.getsampwidth()),
            channels=self.wf.getnchannels(),
            rate=self.wf.getframerate(),
            output=True
        )

    def play(self):
        """ Play entire file """
        self.wf.rewind()
        data = self.wf.readframes(self.chunk)

        while data:
            self.stream.write(data)
            data = self.wf.readframes(self.chunk)

    def close(self):
        """ Graceful shutdown """
        self.stream.close()
        self.p.terminate()


url = "https://app.resemble.ai/api/v1/projects/b9371d23/clips"
headers = {
    'Authorization': 'Token token="1x2oZ7SuwbuqXk1trIcJogtt"',
    'Content-Type': 'application/json'
}
response = requests.get(url, headers=headers).json()

clips = {}

# Load the possible clips files into a list
for clip in response['pods']:
    title = clip['title'].replace(" ", "")

    if title not in clips:
        clips[title] = {
            'title': title,
            'uuid': clip['uuid'],
            'link': clip['link'],
            'finished': clip['finished']
        }
    else:
        print(f"Warning: A clip with the name {title} has already been loaded")


# Load the audio file of a clip from a folder
def get_clip(clip_name, clip_folder_name):
    if clip_name in clips:
        audio_clip = clips[clip_name]
        audio_file = None

        if clip_folder_name and not os.path.isdir("AudioFiles/" + clip_folder_name):
            os.mkdir("AudioFiles/" + clip_folder_name)

        clip_folder_name = "AudioFiles/" + clip_folder_name

        if os.path.isfile(clip_folder_name + "/" + clip_name + ".wav"):
            audio_file = AudioFile(clip_folder_name + "/" + clip_name + ".wav")
        else:
            if clip['finished']:
                with requests.Session() as req:
                    download = req.get(audio_clip['link'], headers=headers)

                    if download.status_code == 200:
                        with open(clip_folder_name + "/" + clip_name + ".wav", 'wb') as f:
                            f.write(download.content)
                    else:
                        print(f"Could not download audio file {clip_name}")
                audio_file = AudioFile(clip_folder_name + "/" + clip_name + ".wav")
                print(f"Audio File {clip_name} successfully downloaded")
            else:
                print(f"Error: The audio file {clip_name} has not been created. Go to Resemble.ai and create the file.")
        return audio_file
    else:
        print(f"Error: The clip {clip_name} does not exist.")


audio_files = {}

if not os.path.isdir("AudioFiles"):
    os.mkdir("AudioFiles")

# Number
for i in range(1, 61):
    audio_files["Number" + str(i)] = get_clip("Number" + str(i), "Number")

# Greeting
for i in range(1, 4):
    audio_files["Greeting" + str(i)] = get_clip("Greeting" + str(i), "Greeting")

# Offer Help
audio_files["OfferHelp"] = get_clip("OfferHelp", "OfferHelp")

# Timer
audio_files["TimerInvalidFormat"] = get_clip("TimerInvalidFormat", "Timer")
audio_files["TimerSet"] = get_clip("TimerSet", "Timer")
audio_files["And"] = get_clip("And", "Timer")
audio_files["Hour"] = get_clip("Hour", "Timer")
audio_files["Hours"] = get_clip("Hours", "Timer")
audio_files["Minute"] = get_clip("Minute", "Timer")
audio_files["Minutes"] = get_clip("Minutes", "Timer")
audio_files["Second"] = get_clip("Second", "Timer")
audio_files["Seconds"] = get_clip("Seconds", "Timer")

# World Time
audio_files["In"] = get_clip("In", "WorldTime")
audio_files["ItIs"] = get_clip("ItIs", "WorldTime")
audio_files["O"] = get_clip("O", "WorldTime")

audio_files["Denmark"] = get_clip("Denmark", "WorldTime")
audio_files["Copenhagen"] = get_clip("Copenhagen", "WorldTime")
audio_files["England"] = get_clip("England", "WorldTime")
audio_files["London"] = get_clip("London", "WorldTime")

# Wikipedia
audio_files["SearchingWikipedia"] = get_clip("SearchingWikipedia", "Wikipedia")
audio_files["AccordingtoWikipedia"] = get_clip("AccordingtoWikipedia", "Wikipedia")

# Open Webpage
audio_files["OpeningWebpage"] = get_clip("OpeningWebpage", "Webpage")
audio_files["WebpageNotFound"] = get_clip("WebpageNotFound", "Webpage")

with open("Data/KnownWebpages.json") as known_webpages:
    webpage_names = json.load(known_webpages)

    for webpage in webpage_names:
        audio_files[webpage['name'].replace(" ", "")] = get_clip(webpage['name'].replace(" ", ""), "Webpage")
    known_webpages.close()

# News
audio_files["News"] = get_clip("News", "News")

# Weather
audio_files["CurrentWeather"] = get_clip("CurrentWeather", "Weather")
audio_files["Is"] = get_clip("Is", "Weather")
audio_files["WeatherTemperature"] = get_clip("WeatherTemperature", "Weather")
audio_files["WeatherDegrees"] = get_clip("WeatherDegrees", "Weather")

with open('Data/WeatherDescriptions.txt', 'r') as weather_descriptions:
    for description in weather_descriptions.readlines():
        audio_files[description.strip().replace(" ", "")] = get_clip(description.strip().replace(" ", ""), "Weather")
    weather_descriptions.close()

# Initialize the pyttsx3 library
engine = pyttsx3.init()
voices = engine.getProperty('voices')  # gets the voices for Jarvis

# Jarvis's voice
for voice in voices:
    if voice.languages[0] == 'en_GB':
        engine.setProperty('voice', voice.id)
        break

rate = engine.getProperty('rate')
engine.setProperty('rate', 180)

volume = engine.getProperty('volume')
engine.setProperty('volume', 0.6)


# This function enables Jarvis to speak
def speak(text):
    engine.say(text)
    engine.runAndWait()


# play audio file or use pyttsx3 instead if the audio file is not available
def play_audio(audio_name, text):
    if audio_name in audio_files and audio_files[audio_name]:
        audio_files[audio_name].play()
    else:
        speak(text)


# This function enables Jarvis to take commands
def take_command(respond=True):
    recognition = sr.Recognizer()

    with sr.Microphone() as source:
        recognition.adjust_for_ambient_noise(source)  # reduce noise
        print("Listening...")

        # this try function will help Jarvis understand what the user is saying
        try:
            audio = recognition.listen(source,
                                       timeout=6)  # uses the function to listen for audio from speech_recognition library
            input_statement = recognition.recognize_google(audio, language='en_GB')
            print(f"{input_statement}")

        # This exception will prevent run time errors
        except sr.RequestError:
            # API was unreachable or unresponsive
            print("API was unreachable or unresponsive")
            return ""
        except sr.UnknownValueError:
            # speech was unintelligible
            if respond:
                speak("Pardon me, could you repeat that?")
            return ""
        except sr.WaitTimeoutError:
            # Time out
            return ""
        return input_statement


# This function allows Jarvis to greet the user
def greet_user():
    hour = datetime.datetime.now().hour  # gets the current hour

    # This if statements checks the time and gives a shutting response
    if 0 <= hour < 10:
        play_audio("Greeting1", "Good morning sir, I hope you slept well")
    elif 10 <= hour < 12:
        play_audio("Greeting1", "Good morning sir")
    elif 12 <= hour < 18:
        play_audio("Greeting2", "Good afternoon sir")
    else:
        play_audio("Greeting3", "Good evening sir")

    time.sleep(0.4)
    print("How may I help you?")
    play_audio("OfferHelp", "How may I help you?")


"""
# This section controls the light
b = Bridge('10.24.9.200')
b.connect()
b.get_api()


def turn_lights_on_and_off_controls(user_light_command):
    with open('Data/LightControls.json', 'r') as lc:
        light_command = json.load(lc)

        # Turn lights on, commands
        for lightsOn in light_command['TurnOnLights']:
            if lightsOn['command'].lower() in user_light_command:
                b.set_group(1, 'on', True)
        # Turn lights off, commands
        for lightsOff in light_command['TurnOffLights']:
            if lightsOff['command'].lower() in user_light_command:
                b.set_group(1, 'on', False)
        # Turn on the firs light, command
        for firstLightOn in light_command['LightBulbOn1']:
            if firstLightOn['command'].lower() in user_light_command:
                b.set_light(1, 'on', True)
        # Turn off the first light, command
        for firstLightOff in light_command['LightBulbOff1']:
            if firstLightOff['command'].lower() in user_light_command:
                b.set_light(1, 'on', False)
        # Turn on the second light, command
        for secondLightOn in light_command['LightBulbOn2']:
            if secondLightOn['command'].lower() in user_light_command:
                b.set_light(2, 'on', True)
        # Turn off the second light, command:
        for secondLightOff in light_command['LightBulbOff2']:
            if secondLightOff['command'].lower() in user_light_command:
                b.set_light(2, 'on', False)
        # Turn on the third light, command
        for thirdLightOn in light_command['LightBulbOn3']:
            if thirdLightOn['command'].lower() in user_light_command:
                b.set_light(3, 'on', True)
        # Turn off teh third light, command
        for thirdLightOff in light_command['LightBulbOff3']:
            if thirdLightOff['command'].lower() in user_light_command:
                b.set_light(3, 'on', False)
        # Turn on the fourth light, command
        for fourthLighton in light_command['LightBulbOn4']:
            if fourthLighton['command'].lower() in user_light_command:
                b.set_light(4, 'on', True)
        # Turn of the fourth light, command
        for fourthLightOff in light_command['LightBulbOff4']:
            if fourthLightOff['command'].lower() in user_light_command:
                b.set_light(4, 'on', False)
"""


# This function allows Jarvis to set a timer from user specifications
def timer(input_statement):
    words = input_statement.replace(",", "").replace("-", " ").split()
    invalid_time_format = False
    values_list = {}
    duration = 0

    # Loop through every word in the statement and look for digits and
    # check if the word after the digit matches one of the keywords
    for k in range(0, len(words)):
        if words[k].isdigit() and k + 1 < len(words):
            word = words[k + 1] if words[k + 1][-1] != "s" else words[k + 1][:len(words[k + 1]) - 1]

            if word == "second" or word == "minute" or word == "hour":
                if word not in values_list:
                    values_list[word] = max(0, int(words[k]))
                    values_list[word + "_count"] = 1
                else:
                    values_list[word + "_count"] += 1

    resorted_values = {}

    # Reorganize values so it's in the order of hour, minute, second
    if 'hour' in values_list:
        resorted_values['hour'] = values_list['hour']
        resorted_values['hour_count'] = values_list['hour_count']
    if 'minute' in values_list:
        resorted_values['minute'] = values_list['minute']
        resorted_values['minute_count'] = values_list['minute_count']
    if 'second' in values_list:
        resorted_values['second'] = values_list['second']
        resorted_values['second_count'] = values_list['second_count']

    timer_text = "A timer has now been set for"

    # Construct the message that'll notify the user about the timer
    for word in resorted_values:
        if word in input_statement and values_list[word] > 0:
            if values_list[word + "_count"] <= 1:
                duration += values_list[word] * (1 if word == "second" else (60 if word == "minute" else 3600))
                timer_text += " " + str(values_list[word]) + " " + word + ("s" if values_list[word] > 1 else "") + ","
            else:
                invalid_time_format = True

    timer_text = ' and'.join(timer_text[:-1].rsplit(',', 1))

    # If the timer contains multiple instances of the same keyword the format given is invalid
    if invalid_time_format:
        print("Invalid time format.")
        play_audio("TimerInvalidFormat",
                   "I'm sorry but I can't start a timer with those specifications")
        return

    hours, reminder = divmod(duration, 3600)
    minutes, secs = divmod(reminder, 60)

    print("Timer: {:02d}:{:02d}:{:02d}".format(hours, minutes, secs))
    play_audio("TimerSet", timer_text)

    timer_text_words = timer_text.split(" ")

    for word in timer_text_words:
        if "and" in word or "hour" in word or "minute" in word or "second" in word:
            play_audio(word.capitalize(), "")
        elif word.isdigit():
            play_audio("Number" + word, word)

    # Run the timer
    while duration:
        hours, reminder = divmod(duration, 3600)
        minutes, secs = divmod(reminder, 60)
        print("{:02d}:{:02d}:{:02d}".format(hours, minutes, secs))
        time.sleep(1)
        duration -= 1

    print("It is time")
    speak("It is time")


# This function allows Jarvis to tell the time of a capital around the world
def world_and_local_time(input_statement):
    with open("Data/TimeZones.json", 'r') as j:
        time_zone = json.load(j)

        # Loop through every continent and every country and tell the time of that country's capital
        for continent in time_zone:
            for country in time_zone[continent]:
                if country['name'].lower() in input_statement or 'capital' in country and country[
                    'capital'].lower() in input_statement:
                    country_capital = country['capital'] if 'capital' in country else ''
                    time_string = continent + "/" + country_capital
                    country_time = pytz.timezone(time_string)
                    current_time = datetime.datetime.now(country_time).strftime("%H:%M")
                    print("In " + f"{country_capital}, " + f"{country['name']}, it's " + f"{current_time}")

                    if country['name'] in audio_files or country_capital in audio_files:
                        play_audio("In", "")
                        play_audio(country_capital, country_capital)
                        time.sleep(0.4)
                        play_audio(country['name'], country['name'])

                        current_time_list = current_time.split(":")
                        play_audio("ItIs", "")

                        for d in range(0, 2):
                            hand_time = current_time_list[d][0].replace("0", "") + current_time_list[d][1]

                            if d == 1 and len(hand_time) == 1:
                                play_audio("O", "")

                            play_audio("Number" + hand_time, "")
                    else:
                        speak("In " + f"{country_capital}, " + f"{country['name']}, it's " + f"{current_time}")
                    return

        # If no country or capital was found in the input statement, simply tell the time of the default capital
        country_time = pytz.timezone("Europe/Copenhagen")
        current_time = datetime.datetime.now(country_time).strftime("%H:%M")
        print("It's " + f"{current_time}")
        current_time_list = current_time.split(":")
        play_audio("ItIs", "It's")

        for d in range(0, 2):
            hand_time = current_time_list[d][0].replace("0", "") + current_time_list[d][1]

            if d == 1 and len(hand_time) == 1:
                play_audio("O", "O")

            play_audio("Number" + hand_time, hand_time)


# This function will enable the user to search the wikipedia for answers
def search_wikipedia(input_statement):
    search_text = input_statement[input_statement.index('wikipedia') + len('wikipedia') + 1:]

    while not search_text:
        speak("Pardon me, could you repeat that?")
        input_statement = take_command().lower()

        if "wikipedia" in input_statement:
            search_text = input_statement[input_statement.index('wikipedia') + len('wikipedia') + 1:]
        else:
            search_text = input_statement

    play_audio("SearchingWikipedia", "Searching Wikipedia")
    result = wikipedia.summary(search_text, sentences=4)
    play_audio("AccordingtoWikipedia", "According to wikipedia")
    print(result)
    speak(result)


# Open a webpage in google
def open_webpages(input_statement):
    # Checks if a known webpage is in the JSON-file
    for known_webpage in webpage_names:
        if known_webpage['name'].lower() in input_statement:
            play_audio("OpeningWebpage", "Opening")
            play_audio(known_webpage['name'], known_webpage['name'])
            webbrowser.open_new_tab(known_webpage['link'])
            return

    play_audio("WebpageNotFound", "The webpage you are looking for don't exist in my list")

    search_text = input_statement[input_statement.index('open') + len('open') + 1:]
    result_list = search(query=search_text, tld="co.in", lang="en", num=3, start=0, stop=3, pause=2.0)

    for result in result_list:
        print(result)


# Open a news site
def news(input_statement):
    webbrowser.open_new_tab("https://www.dr.dk/")
    play_audio("News", "Here are some news from Dr.dk")


# Tell the weather in a given capital
def weather(input_statement):
    city_name = "Copenhagen"

    with open("Data/TimeZones.json", 'r') as j:
        time_zone = json.load(j)

        for continent in time_zone:
            for country in time_zone[continent]:
                if country['name'].lower() in input_statement or 'capital' in country and country[
                    'capital'].lower() in input_statement:
                    city_name = country[
                        'capital'] if 'capital' in country else country['name']

    api_key = "826b9c92900e4a8a99571c3665261da6"
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    complete_url = base_url + "?q=" + city_name + "&appid=" + api_key
    api_response = requests.get(complete_url)
    api_response = api_response.json()

    # --Possible Descriptions--

    # clear sky
    # few clouds
    # scattered clouds
    # broken clouds
    # shower rain
    # rain
    # thunderstorm
    # snow
    # mist

    if api_response["cod"] != 404:
        location = api_response['name']
        temperature = round(api_response['main']['temp'] - 273.15)
        weather_description = " ".join([
            word.capitalize()
            for word in api_response['weather'][0]['description'].split(" ")
        ])

        print(("The current weather in {0} is {1} with a temperature of {2} " +
               "degrees Celsius").format(location, weather_description, temperature))

        play_audio("CurrentWeather", "The current weather in")
        play_audio(city_name, city_name)
        play_audio("Is", "Is")
        play_audio(weather_description.replace(" ", ""), weather_description)
        play_audio("WeatherTemperature", "With a temperature of")
        play_audio("Number" + str(temperature), str(temperature))
        play_audio("WeatherDegrees", "Degrees Celsius")


# Answer a mathematical or geographical question
def math(input_statement):
    input_statement = input_statement[input_statement.index('what is'):]
    print("Searching...")
    speak("Searching...")
    app_id = "X8K53V-A95P9W6UVW"
    client = wolframalpha.Client(app_id)
    res = client.query(input_statement)

    try:
        answer = next(res.results).text.split("\n")[0].split(",")[0]
        answer = answer[answer.rfind("|")+2:].capitalize()

        print(answer)

        if answer.isdigit():
            play_audio("Number" + answer, answer)
        else:
            play_audio(answer, answer)

    except StopIteration:
        speak("I'm sorry but I don't know the answer to that question")


# The things Jarvis shall do on start up
print("Loading your personal assistant Jarvis")

# Checks if the name of the file equals the main file.
if __name__ == '__main__':
    while True:
        statement = take_command(respond=False).lower()  # Allows Jarvis to hear what you're saying

        if statement and ("hey jarvis" in statement or "hello there" in statement):
            greet_user()
            statement = take_command().lower()

            while not statement:
                statement = take_command().lower()
        else:
            continue

        if "nevermind" in statement or "nothing" in statement:
            speak("Okay")
            continue

        goodbye = False

        with open("Data/GoodByeSayings.txt", 'r') as file:
            for goodbye_saying in file.readlines():
                if goodbye_saying.strip() in statement:
                    goodbye = True
                    break

        if goodbye:
            print("Okay, see you later")
            speak("Okay, see you later")
            break

        # Set timer
        if "timer" in statement:
            timer(statement)

        # Give the time
        elif "time" in statement:
            world_and_local_time(statement)

        # Light controls
        # elif "light" in statement:
        # turn_lights_on_and_off_controls(statement)

        # Searching wikipedia for questions
        elif 'wikipedia' in statement:
            search_wikipedia(statement)

        # Open a webpage
        elif "open" in statement:
            open_webpages(statement)

        # news
        elif 'news' in statement:
            news(statement)

        # search google

        # Forecasting the weather
        elif 'weather' in statement:
            weather(statement)

        # Math
        elif 'what is' in statement or "what's" in statement:
            math(statement.replace("what's", "what is"))

        else:
            speak("I'm sorry but I can't help you with that")
