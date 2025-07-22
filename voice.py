import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os

# Initialize engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Female voice (optional)
engine.setProperty('rate', 170)  # Speed

def speak(text):
    engine.say(text)
    engine.runAndWait()

def greet():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("I am your assistant. How can I help you?")

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        command = r.recognize_google(audio, language="en-in")
        print(f"You said: {command}")
    except:
        speak("Sorry, I didn't catch that. Please say again.")
        return "None"
    return command.lower()

def run_assistant():
    greet()
    while True:
        command = take_command()

        if "time" in command:
            time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The time is {time}")

        elif "open youtube" in command:
            webbrowser.open("https://www.youtube.com")
            speak("Opening YouTube")

        elif "open google" in command:
            webbrowser.open("https://www.google.com")
            speak("Opening Google")

        elif "play music" in command:
            music_dir = "C:\\Users\\YourName\\Music"  # Change path
            songs = os.listdir(music_dir)
            os.startfile(os.path.join(music_dir, songs[0]))

        elif "exit" in command or "quit" in command:
            speak("Goodbye!")
            break

        else:
            speak("Sorry, I can't perform that task yet.")

# Start assistant
run_assistant()
