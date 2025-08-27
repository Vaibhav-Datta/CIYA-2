import datetime
import speech_recognition as sr
from playsound import playsound
import os
import webbrowser
import time
import ollama
import asyncio
from edge_tts import Communicate

history = []
model = "phi3:mini"

# Functions

# Delete History to make Ollama response faster
MAX_HISTORY = 6  # Keep last 3 user+assistant turns

def trim_history():
    global history
    if len(history) > MAX_HISTORY:
        history = history[-MAX_HISTORY:]


# Speak function
def speak(audio):
    print(f"Ciya says: {audio}")
    try:
        async def run_tts():
            communicate = Communicate(
                text=audio,
                voice="en-US-JennyNeural",  
                rate="-20%"               
            )
            await communicate.save("ciya_response.mp3")

        asyncio.run(run_tts())
        playsound("ciya_response.mp3")
        time.sleep(0.5)
        os.remove("ciya_response.mp3")
    except Exception as e:
        print(f"Speech error: {e}")

# Greet according to time
def greet():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good morning sir I am CIYA, pronounced as Siya, I am a personal assistant created by Mr. V.")
    elif 12 <= hour < 18:
        speak("Good afternoon sir I am CIYA, pronounced as Siya, I am a personal assistant created by Mr. V.")
    else:
        speak("Good evening sir I am CIYA, pronounced as Siya, I am a personal assistant created by Mr. V.")

# Listenig & Recognizing
def takeCommand():
    r = sr.Recognizer()
    r.energy_threshold = 100
    r.phrase_threshold = 0.3
    with sr.Microphone() as source:
        r.pause_threshold = 1
        print("CIYA is listening...")
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-IN')
        print(f"User said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        return "none"
    except sr.RequestError:
        speak("Sorry, I'm having trouble connecting to the recognition service.")
        return "none"

# Memory (storing and fetching data)
def save_memory(data):
    with open("memory.txt", "w") as file:
        file.write(str(data))

def load_memory():
    try:
        with open("memory.txt", "r") as file:
            content = file.read()
            return eval(content) if content else {}
    except FileNotFoundError:
        return {}

# Command mode

def command_mode():
    global history
    while True:
        command = takeCommand()

        if command == "none":
            continue

        # Exit Commands
        if any(phrase in command for phrase in ["exit","sleep","go to sleep","activate sleep mode","ciya stop","eva stop","stop listening","stop responding","no more commands","goodbye","exit assistant","terminate","ciya exit","eva exit","ciya ruk ja","eva ruk ja","ruk ja"]):
            speak("Okay sir, going back to sleep.")
            break

        elif any(phrase in command for phrase in ["chup", "chup reh", "chup re"]):
            speak("Sorry sir, my mistake. Please forgive me.")
            break

# CHAT Mode

        elif "chat" in command:
            speak("CHAT Mode Activated")
            history = [
                 {
                    "role": "system",
                    "content": "You are a helpful voice based personal assistant and your name is CIYA (pronunced as siya) and you are made or created by V. You can do or perform various tasks like google search, remember info, open apps, tell current time, remember what you say, store info under certain keywords and power off your system. Please keep your responses concise—no more than 2–3 sentences and reply fast."
                }
            ]
            while True:
                user_input = takeCommand()
                if user_input == "none":
                    continue
                if "exit" in user_input:
                    speak("Exiting CHAT Mode and switching to Command Mode sir")
                    break

                message = {
                    "role": "user",
                    "content": user_input
                }

                history.append(message)
                trim_history() 
                response = ollama.chat(model=model, messages=history)
                bot_message_content = response.message.content
                speak(bot_message_content)

                bot_message = {
                    "role": "assistant",
                    "content": bot_message_content
                }
                history.append(bot_message)
                trim_history()

        # Hi
        elif any(phrase in command for phrase in ["hi ciya", "hi","introduction", "introduce", "what are you", "who are you", "hello"]):
            speak("Hello, I am a personal assistant created by Mr. V, I can perform various tasks like google search, remembering info, opening your apps, tell you current time, remember what you say, store info under certain keywords and power off your system")

        # Poweroff
        elif "shutdown" in command or "power off" in command or "turn off" in command:
            speak("Shutting down your system...")
            os.system("shutdown /s /f /t 0")

        # Google search

        elif any(phrase in command for phrase in ["search"]):
            query = command.replace("search", "").strip()
            
            if query:
                speak("Searching Google...")
                webbrowser.open(f"google.com/search?q={query}")
            else:
                speak("What would you like me to search for?")
                query = takeCommand()
                if query != "none":
                    webbrowser.open(f"google.com/search?q={query}")

        # Opening Commands
        elif any(phrase in command for phrase in ['open gmail', 'mail','email']):
            speak('Opening Gmail sir.')
            webbrowser.open("gmail.com")

        elif any(phrase in command for phrase in ['open whatsapp', 'whatsapp']):
            speak('Opening WhatsApp Web sir.')
            webbrowser.open("web.whatsapp.com")
    
        elif any(phrase in command for phrase in ['open youtube', 'youtube', 'yt']):
            speak('Opening YouTube sir')
            webbrowser.open("youtube.com")

        elif any(phrase in command for phrase in ['open google', 'siya open google']):
            speak('Opening Google sir')
            webbrowser.open("google.com")

        # Tells Time
        elif "the time" in command:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"It's {strTime}")

        # Compliment reply            
        elif any(phrase in command for phrase in ["good job", "excellent", "good", "nice work"]):
            speak("Thank you sir")

        # Remembers voice input            
        elif "remember" in command:
            memory = load_memory()
            to_remember = command.replace("remember", "").strip()
            if to_remember:
                memory['remembered'] = to_remember
                save_memory(memory)
                speak("Okay, I will remember that sir.")
            else:
                speak("What should I remember, sir?")

        elif any(phrase in command for phrase in ["recall", "bola tha", "yad kr"]):
            memory = load_memory()
            if 'remembered' in memory:
                speak(f"You asked me to remember: {memory['remembered']}")
            else:
                speak("Sorry, I don't have anything remembered yet.")

        # Saves info as Key and Value (Dictionery logic)
        elif 'open memory' in command:
            memory = load_memory()
            speak("Would you like to save something or get something?")
            follow_up = takeCommand()

            # Saving Key
            if any(phrase in follow_up for phrase in ['save', 'store', 'key']):
                speak("Please specify a key")
                key = takeCommand()

                if key == "none":
                    speak("Sorry, I didn't catch that.")
                else:
                    speak(f"Okay, what should I save under '{key}'?")
                    value = takeCommand()

                    if value == "none":
                        speak("Sorry, I didn't catch that.")
                    else:
                        memory[key] = value
                        save_memory(memory)
                        speak(f"Got it! I've saved '{value}' under '{key}'.")

            # Retrieving Value
            elif any(phrase in follow_up for phrase in ['get', 'retrieve', 'value']):
                speak("What information do you want me to get? Please say the key.")
                key = takeCommand()

                if key == "none":
                    speak("Sorry, I didn't catch that.")
                else:
                    value = memory.get(key)
                    if value:
                        speak(f"Your value for the key {key} is : {value}")
                    else:
                        speak(f"Sorry, I don't have anything saved under '{key}'.") 

                            
# Ollama fallback response
        else:
            message = {
                "role": "user",
                "content": command
            }

            history.append(message)
            trim_history() 
            response = ollama.chat(model=model, messages=history)
            bot_message_content = response.message.content
            speak(bot_message_content)

            bot_message = {
                "role": "assistant",
                "content": "You are a helpful voice based personal assistant and your name is CIYA (pronounced as siya) and you are made or created by V. You can do or perform various tasks like google search, remember info, open apps, tell current time, remember what you say, store info under certain keywords and power off your system. Please keep your responses concise—no more than 2–3 sentences and reply fast." + bot_message_content
            }
            history.append(bot_message)
            trim_history() 

# CT Widget Connection

def start_assistant():
    speak("Please say wake up to activate Command Mode")

    # Sleep Mode
    while True:
        print("|CIYA|\nCustomizable Interface for your Access\nSTANDBY MODE")
        query = takeCommand()

        if query == "none":
            continue

        # Turn off (Exiting CIYA)
        if "power off" in query:
            speak("Turning off sir")
            break

        # To let user know that sleep mode is ALREADY ACTIVE
        if "exit" in query:
            speak("Sleep mode is active sir")

        # Switiching to Command Mode from Sleep
        if "wake up" in query or "wake" in query or "siya" in query or "power on" in query:
            greet()
            command_mode()

# If you don't want widget and want to run code directly 
if __name__ == "__main__":
    start_assistant()