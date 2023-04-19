import cmd
import subprocess
import sys
import pyttsx3 
import speech_recognition as sr
import datetime
import wikipedia 
import webbrowser
import os
import smtplib
#import openai as ai
# for GUI : 
from PyQt5 import QtWidgets, QtCore,QtGui
from PyQt5.QtCore import QTimer,QTime,QDate, Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from madhavUI import Ui_MadhavUI # from UI file [madhavUI.py] we are importing Ui_MadhavUI class 

###########Importing other python files#######
from difflib import get_close_matches
import json
from random import choice
#from web_scrapping import latestNews()
 


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate',180)

#function for speak (text to speech)
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

class DateTime:
	def currentTime(self):
		time = datetime.datetime.now()
		x = " A.M."
		if time.hour>12: x = " P.M."
		time = str(time)
		time = time[11:16] + x
		return time

	def currentDate(self):
		now = datetime.datetime.now()
		day = now.strftime('%A')
		date = str(now)[8:10]
		month = now.strftime('%B')
		year = str(now.year)
		result = f'{day}, {date} {month}, {year}'
		return result

#function to wish me 
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning sir!")
    elif hour>=12 and hour<18:
        speak("Good Afternoon sir!")   
    else:
        speak("Good Evening sir!")  
#function to translate 
def lang_translate(text,language):
	from googletrans import Translator, LANGUAGES
	if language in LANGUAGES.values():
		translator = Translator()
		result = translator.translate(text, src='en', dest=language)
		return result
	else:
		return "None"


data = json.load(open('assets/normal_chat.json', encoding='utf-8'))
def reply(query):
	if query in data:
		response =  data[query]
	else:
		query = get_close_matches(query, data.keys(), n=2, cutoff=0.6)
		if len(query)==0: return "None"
		return choice(data[query[0]])
	return choice(response)

#function to send email from my email id and password
def sendEmail(to, content):  
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login("uttamadha123@gmail.com", "Officialuttam@123")
    server.sendmail("uttamadha123@gmail.com", to, content)
    server.close()

class MainThread(QThread):
    def __init__(self):
        super(MainThread,self).__init__()

    def run(self):
        #self.TaskExecution()   (with this direct program will start )
        #start program with my command: 
        speak("Your personal Assistent program started. Waiting for your command.")
        while True:
            self.query = self.takeCommand()
            if "wake up" in self.query or "let's start madhav" in self.query or "hello madhav" in self.query:
                speak("for u always up sir")
                print("for u always up sir")
                self.TaskExecution()
         
#function to take commands from me(work as ears)
    def takeCommand(self):
        #It takes microphone input from the user and returns output
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source)
        try:
            print("Recognizing sir...")
            query = r.recognize_google(audio, language='en-in')
            print(f"you said: {query}\n")
        except Exception as e:
            print("Say that again sir...") 
            return "None"
        return query

    def TaskExecution(self):
        wishMe()
        speak("What We are doing today sir.") 
        while True:
            self.query = self.takeCommand().lower()


############# get information : ###########
        #1) using wikipedia
            if 'tell me about' in self.query:
                speak('Searching Wikipedia about this sir')
                self.query = self.query.replace("wikipedia", "")
                results = wikipedia.summary(self.query, sentences=2)
                speak("According to Wikipedia")
                print(results)
                speak(results)

            elif 'open google' in self.query:
                speak('What do you want to search on google')
                cm = self.takeCommand()
                webbrowser.open(f"{cm}")
                speak("Openning google and searching"+f"{cm}" +"sir please wait..")
            
            #elif 'news' in self.query:
             #   speak('Getting the latest news...')
              #  headlines,headlineLinks = web_scrapping.latestNews(2)
               # for head in headlines: speak(head, True)
               # speak('Do you want to read the full news?', True)
                #text = self.takeCommand()
              #  if 'no' in self.query:
               #     speak("No Problem sir")
                #else:
                #    speak("Ok, Opening browser...", True)
                #    web_scrapping.openWebsite('https://indianexpress.com/latest-news/')
                #    speak("You can now read the full news from this website.")
                #return

            elif 'translate' in self.query:
                speak("What do you want to translate?", True, True)
                sentence = self.takeCommand()
                speak("Which langauage to translate ?", True)
                langauage = self.takeCommand()
                result = lang_translate(sentence, langauage)
                if result=="None": speak("This langauage doesn't exists")
                else:
                    speak(f"In {langauage.capitalize()} you would say:", True)
                    if langauage=="hindi":
                        print(result.text, True)
                        speak(result.pronunciation)
                    else: speak(result.text, True)
                return


    #working on youtube
            elif 'open youtube' in self.query:
                webbrowser.open("www.youtube.com")
                speak("Opening Youtube sir please wait..")
                
            
            elif 'open my chrome' in self.query:
                codePath= "C:\\Users\\Dell\\Documents\\Uttam (uttam adha) - Chrome"
                os.startfile(codePath)

    #music
            elif 'play music' in self.query:
                music_dir = 'D:\\Music'
                songs = os.listdir(music_dir)
                speak("Playing Songs sir please wait..")
                print(songs)    
                os.startfile(os.path.join(music_dir, songs[5]))

            
    #working on myfiles
            elif 'open my web dev folder' in self.query:
                codePath= "C:\\Users\\Dell\\Desktop\\web dev"
                os.startfile(codePath)

            elif 'open my movies' in self.query:
                codePath = "D:\MY movies"
                os.startfile(codePath)
                speak("Opening your movies folder sir..")
            



    #sending mail to person

            elif 'email to harsh' in self.query:
                try:
                    speak("What should I say?")
                    content = self.takeCommand()
                    print(content)
                    to = "harshparmar4760@gmail.com"    
                    sendEmail(to, content)
                    speak("Email has been sent!")
                except Exception as e:
                    print(e)
                    speak("Sorry!! I am not able to send this email")


    #closing program
            elif 'close the program' in self.query:
                speak("Closing program sir,..see you afterwards.")
                codePath= "C:\\Users\\Dell\\Desktop\\AI\\Python code\\jarvisdemo.py"
                os.closefile(codePath)

############Smart replies#######
            if 'morning' in self.query or 'evening' in self.query or 'noon' in self.query:
                wishMe()
                return
		
            result = reply(self.query)
            if result != "None": speak(result, True, True)
            else:
                speak("I don't know anything about this. Do you want to search it on web?", True, True)
                response = self.takeCommand()
                if 'no' in self.query:
                    speak("Ok ")
                else:
                    speak("Here's what I found on the web... ")
                   # web_scrapping.googleSearch(text)
                


startExecution = MainThread()

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MadhavUI()  # calling GUI
        self.ui.setupUi(self) 
        self.ui.pushButton.clicked.connect(self.startTask) #will change to voice command which will activate madhav program.
        self.ui.pushButton_2.clicked.connect(self.close)

    def startTask(self):
        self.ui.movie = QtGui.QMovie("C:\\Users\\Dell\\Desktop\\AI\\MadhavAI\\UI designs\\QjoV.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start() 
        self.ui.movie = QtGui.QMovie("C:\\Users\\Dell\\Desktop\\AI\\MadhavAI\\UI designs\\7LP8.gif")
        self.ui.label_3.setMovie(self.ui.movie) 
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("C:\\Users\\Dell\\Desktop\\AI\\MadhavAI\\UI designs\\Jarvis_Loading_Screen.gif")
        self.ui.label_4.setMovie(self.ui.movie) 
        self.ui.movie.start()
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        #self.ui.textBrowser_3.append('>>')
        #self.ui.textBrowser_3.setText(MainThread.__init__(self))
        #self.ui.textBrowser_3.setText(MainThread.TaskExecution(self))
        startExecution.start()
        

    def showTime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        label_time = current_time.toString('hh:mm:ss')
        label_date = current_date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(label_date)
        self.ui.textBrowser_2.setText(label_time)
  

app = QApplication(sys.argv)
madhavAI = Main()
madhavAI.show()
exit(app.exec_())








