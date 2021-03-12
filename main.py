import speech_recognition as sr
import pyttsx3  # This library converts text into speech
import datetime  # takes the current time of the your time zone and displays it
import wikipedia  # takes the the results that is found on wikipedia
import webbrowser  # allows the assistant to open a new browser
import time  # sets a timer for the program for timeout

# Sapi5 is a Microsoft Text to speech engine used for voice recognition
engine = pyttsx3.init()  # creating the object

voices = engine.getProperty('voices')

for voice in voices:
    print(voice)
    if voice.languages[0] == 'en_GB':
        engine.setProperty('voice', voice.id)
        break


# This is the speak function which allow pur voice assistant to reply to your commands
def speak(text):
    engine.say(text)
    engine.runAndWait()


# This function will greet the user depending on the hour of the day
def greetUser():
    hour = datetime.datetime.now().hour  # Gets the current time of the day and gives a greeting

    if 0 <= hour < 12:
        if hour >= 0 or hour < 9:
            speak("Good morning, did you sleep well?")
            print("Good morning, did you sleep well?")
        else:
            speak("Good morning Sir")
            print("Good morning Sir")
    elif 12 <= hour < 18:
        speak("Good afternoon what can i help you with?")
        print("Good afternoon what can i help you with?")
    else:
        speak("Good evening what can i do for you?")
        print("Good evening what can i do for you?")


# This function will take the commands you give it
def takeCommand():
    recognition = sr.Recognizer()

    with sr.Microphone() as source:
        print('Listening...')
        audio = recognition.listen(source)

        # this try-statement will help you the program under stand what the user are asking/saying
        try:
            statement = recognition.recognize_google(audio, language='en_GB')
            print(f"User said: {statement}\n")

        # makes sure that the occurrence of a runtime error will be minimized
        except Exception as e:
            speak("Pardon me, please say that again")
            return "None"
        return statement


# booting the assistant
print("Loading your personal assistant Bagley")
speak("Loading your personal assistant Bagley")
greetUser()  # calls the greetUser function

# This is the main function of the programme
if __name__ == '__main__':

    while True:
        speak('Tell me how i can help you now')
        statement = takeCommand().lower()

        # Checks if the statement holds anything
        if statement == 0:
            continue

        if "goodbye" in statement or "ok bye" in statement or "stop" in statement or "okay bye" in statement:
            speak("Okay good bye see you soon")
            print("Okay good bye see you soon")
            break

        # skill 1 - fetching data from wikipedia
        if 'wikipedia' in statement:
            speak('Searching Wikipedia....')
            statement = statement.replace('wikipedia', "")
            result = wikipedia.summary(statement, sentences = 3)  # gives the result with 3 lines of text
            speak("According to Wikipedia")
            print(result)
            speak(result)

        # Accessing the web browser, google chrome, g-mail and YouTube
        elif 'open youtube' in statement:
            webbrowser.open_new_tab("https://www.youtube.com")
            speak("YouTube is now open")
            time.sleep(5)

        elif 'open google' in statement:
            webbrowser.open_new_tab("https://www.google.com")
            speak("Google is now open")
            time.sleep(5)

        elif 'open g-mail' in statement or 'open mail' in statement:
            webbrowser.open_new_tab("https://www.gmail.com")
            speak("Your mail er now open")

        # Tell the time
        elif 'what time is it' in statement or 'time' in statement or 'whats the current time' in statement:
            strTime = datetime.datetime.now().strftiem("%H:%M")
            speak(f"The time is {strTime}")

