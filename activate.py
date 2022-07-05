import warnings
import speech_recognition as sr
import pyttsx3
from gtts import gTTS
import playsound
import os
import calendar
import datetime
import random
import wikipedia

warnings.filterwarnings("ignore")
engine=pyttsx3.init()
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)

def talk(audio):
    engine.say(audio)
    engine.runAndWait()

def rec_audio():
    recog=sr.Recognizer()
    with sr.Microphone() as source:
        recog.energy_threshold=10000
        recog.adjust_for_ambient_noise(source,1.2)
        print("Listening....")
        audio =recog.listen(source)

    data=""
    try:
        data=recog.recognize_google(audio)
        print(data)
    except sr.UnknownValueError:
        print("Could not understand the audio")
    except sr.RequestError as ex:
        print("Request Error from Google Speech Recognition"+data)

    return data
rec_audio()

def response(text):
    print(text)
    tts=gTTS(text=text,lang=en)
    audio="Audio.mp4"
    tts.save(audio)
    playsound.playsound(audio)
    os.remove(audio)

def call(text):
    action_call="alice"
    text=text.lower()
    if action_call in text:
        return True
    return False

def today_date():
    now=datetime.datetime.now()
    date_now=datetime.datetime.today()
    week_now=calendar.day_name[date_now.weekday()]
    month_now=now.day
    day_now=now.day
    months=[
        "Janvary","February","March","April","May","June","July","August","September","October","November","December"
    ]
    ordinals=['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th',
                '11th', '12th', '13th', '14th', '15th', '16th', '17th', '18th', '19th',
                '20th', '21st', '22nd', '23rd', '24th', '25th', '26th', '27th', '28th',
                '29th', '30th', '31st']
    return f'Today is {week_now}, {months[month_now-1]} the {ordinals[day_now -1]}.'

def say_hello(text):
    greet=["Hi","hey","hola","greetings","What's up","hello","howdy","what's good","hey there"]
    response=["Hi","hey","hola","greetings","What's up","hello","howdy","what's good","hey there"]
    for word in text.split():
        if word.lower() in greet:
            return random.choice(response)+"."
    return ""

def wiki_person(text):
    list_wiki=text.split()
    for i in range(0,len(list_wiki)):
        if i+3<=len(list_wiki) -1 and list_wiki[i].lower() == "who" and list_wiki[i+1].lower()=="is":
            return list_wiki[i+2]+" "+list_wiki[i+3]


while(True):
    try:
        text=rec_audio()
        speak=" "

        if call(text):
            speak=speak+say_hello(text)

            if "date" in text or "day" in text or "month" in text:
                get_today=today_date()
                speak=speak+" "+ get_today

            elif "time" in text:
                now=datetime.datetime.now()
                meridiem =""
                if now.hour>=12:
                    meridiem= "p m"
                    hour=now.hour-12
                else:
                    meridiem="a m"
                    hour=now.hour
                
                if now.minute<10:
                    minute="0"+str(now.minute)
                else:
                    minute=str(now.minute)
                speak=speak+ " "+"It is "+ str(hour)+ ":" + minute + " " +meridiem + " ."

            elif "wikipedia" in text or "Wikipedia" in text:
                if "who is" in text:
                    person=wiki_person(text)
                    wiki=wikipedia.summary(person, sentence=2)
                    speak=speak+" "+wiki
            
        response(speak)
    except:
        talk("I dont know that")


