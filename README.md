## 🤖 CIYA – Customizable Interface for Your Access 

CIYA is a voice-activated personal assistant built in Python, designed to perform everyday tasks through natural speech interaction. Created by Mr. Vaibhav Datta, CIYA can search the web, remember information, open apps, tell the time, and even shut down your system—all with your voice.

## 🧠 Features 

🎙️ Voice Recognition using Google Speech Recognition

🗣️ Text-to-Speech replies via edge-tts and playsound

🕰️ Time-Based Greetings (Good morning/afternoon/evening)

🔍 Google Search Integration

📧 App Launcher: Gmail, WhatsApp Web, YouTube, Google

⏰ Tells Current Time

📝 Memory System Remembers custom phrases Stores key-value pairs for later retrieval

🛑 Sleep & Shutdown Modes via voice command

💬 Friendly Personality with responses to compliments and greetings


## 🧠 Self-Talking Chat Mode powered by Ollama 

CIYA can now generate its own thoughts and engage in natural conversation Chat mode allows free-form interaction without triggering command logic Responses are concise (2–3 sentences) and fast, using the phi3:mini model


## 🧠 How CIYA Thinks: 

CIYA operates in two distinct modes: Sleep Mode: Waits for activation via phrases like "wake up" or "power on" Command Mode: Executes tasks based on recognized voice commands Chat Mode: Engages in intelligent conversation using Ollama's local LLMs

CIYA uses a dictionary-based memory system to store and retrieve custom data, and now leverages local AI models to simulate independent thinking.


## 💬 Chat Mode Powered by Ollama 

CIYA now integrates with Ollama, a local LLM runtime that allows CIYA to generate responses.

🛑 However responses have certain limitations with respect to the respective module used (like in this one I have used phi3:mini module).


## To enable this feature: 

🔧 Install Ollama Download and install Ollama from https://ollama.com


##📦 Pull the Required Model

bash
ollama pull phi3:mini
This is the default model used for CIYA’s chat mode. You can experiment with other models later. Also make sure to create and environment for it.


## 🧠 Import Ollama in Your Script Make sure your script includes: import ollama


## 🙋‍♂️ Creator 

Developed by Mr. Vaibhav Datta, CIYA is a passion project aimed at making voice interaction more personal, intelligent, and customizable.

## 🗂️ File Structure 

ciya.py – Main assistant script 
memory.txt – Stores remembered data (auto-created) 
README.md – Project documentation

## 🚀 Getting Started Prerequisites Install the required Python packages:

bash
pip install SpeechRecognition edge-tts playsound wikipedia pyaudio

## 🚫 License & Usage 
CIYA is not open source and is not permitted for public use, redistribution, or modification. This project is a private build and intended solely for personal experimentation and development by the creator.
