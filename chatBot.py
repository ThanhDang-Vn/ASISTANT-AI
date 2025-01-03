from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import pyttsx3
import datetime
import speech_recognition as sr
import webbrowser as wb 
import requests 
from bs4 import BeautifulSoup


tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-large")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-large")


bot = pyttsx3.init()
voices = bot.getProperty('voices')
bot.setProperty('voice', voices[1].id)


def speak(audio , rate = 200):
    print("Bot: " + audio) 
    bot.setProperty('rate' , rate) 
    bot.say(audio)
    bot.runAndWait()


def time() :
    time = datetime.datetime.now().strftime("%I : %M : %p")
    speak(time) 


def welcome() :
    time_hour = datetime.datetime.now().hour 
    if time_hour >= 4 and time_hour < 12 :
        speak("Good moring Sir !" )
    elif  time_hour >= 12 and time_hour < 17 :
        speak ("Good afternoon Sir !") 
    else :
        speak ("Hello Sir !") 
    speak("How can i help you ? " ) 


def command():
    c = sr.Recognizer()
    with sr.Microphone() as source:
        c.pause_threshold = 1
        print("Listening...")
        audio = c.listen(source) 
    try:
        query = c.recognize_google(audio, language="en")
        print("You said:", query)
        return query
    except sr.UnknownValueError:
        speak("I can't hear you.")
        speak("Please speak again or type your command.")
        query = str(input('Your command: ')) 
        return query
    


# Example usage
if __name__ == "__main__":
    welcome() 
    while True:
        query = command().lower()
        if "google" in query:
            speak("What should I search Sir ? ")  
            search = command().lower()
            url = f"https://www.google.com/search?q={search}"
            wb.get().open(url) 
            speak(f'Here your {search} on google')   
        elif "youtube" in query:
            speak("What should I search Sir ? ") 
            search = command().lower()
            url = f"https://www.youtube.com/search?q={search}" 
            wb.get().open(url) 
            speak(f'Here your {search} on youtube')
        elif "time" in query:
            time() 
        elif "quit" in query:
            speak("Bot is quiting sir, see you late !")
            quit()   
        elif "bye" in query:
            speak("I got it")
            speak("See you late") 
            quit() 
        elif "your name" in query:
            speak("I don't have my name")   
        else:
            for step in range(1):
                # encode the new user input, add the eos_token and return a tensor in Pytorch
                new_user_input_ids = tokenizer.encode(query + tokenizer.eos_token, return_tensors='pt')
            
                # append the new user input tokens to the chat history
                bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if step > 0 else new_user_input_ids
            
                # generated a response while limiting the total chat history to 1000 tokens, 
                chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
            
                # pretty print last ouput tokens from bot
                speak(format(tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)))
            
            
