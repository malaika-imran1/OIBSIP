
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser

engine = pyttsx3.init()
engine.setProperty("rate", 170)

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
   
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 250
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 0.8

    with sr.Microphone() as source:
        print("Listening... Speak clearly.")
        recognizer.adjust_for_ambient_noise(source, duration=0.3)

        try:
            audio = recognizer.listen(
                source,
                timeout=8,
                phrase_time_limit=6
            )
            command = recognizer.recognize_google(audio, language="en-US")
            print("You said:", command)
            return command.lower()

        except sr.WaitTimeoutError:
            print("No speech detected. Try again.")
        except sr.UnknownValueError:
            print("Speech not understood. Speak a little louder.")
        except sr.RequestError:
            speak("Internet connection problem.")
        return ""

def run_assistant():
    speak("Hello! I am your voice assistant.")

    while True:
        command = listen()

        if "hello" in command:
            speak("Hello! How can I help you?")

        elif "time" in command:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            speak("The time is " + current_time)

        elif "date" in command:
            today = datetime.datetime.now().strftime("%d %B %Y")
            speak("Today's date is " + today)

        elif "open google" in command:
            speak("Opening Google.")
            webbrowser.open("https://www.google.com")

        elif "open youtube" in command:
            speak("Opening YouTube.")
            webbrowser.open("https://www.youtube.com")

        elif "stop" in command or "exit" in command or "goodbye" in command:
            speak("Goodbye!")
            break

        elif command:
            speak("Sorry, I do not know that command yet.")

if __name__ == "__main__":
    run_assistant()