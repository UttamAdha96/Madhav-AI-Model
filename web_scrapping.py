import wikipedia
import webbrowser
import requests
from bs4 import BeautifulSoup
import smtplib
import urllib.request
import os
from geopy.geocoders import Nominatim
from geopy.distance import great_circle



class WEATHER:
	def __init__(self):
		self.tempValue = ''
		self.city = ''
		self.currCondition = ''
		self.speakResult = ''

	def updateWeather(self):
		res = requests.get("https://ipinfo.io/")
		data = res.json()
		# URL = 'https://weather.com/en-IN/weather/today/l/'+data['loc']
		URL = 'https://weather.com/en-IN/weather/today/'
		result = requests.get(URL)
		src = result.content

		soup = BeautifulSoup(src, 'html.parser')

		city = ""
		for h in soup.find_all('h1'):
			cty = h.text
			cty = cty.replace('Weather','')
			self.city = cty[:cty.find(',')]
			break

		spans = soup.find_all('span')
		for span in spans:
			try:
				if span['data-testid']=="TemperatureValue":
					self.tempValue = span.text[:-1]
					break
			except Exception as e:
				pass

		divs = soup.find_all('div', class_='CurrentConditions--phraseValue--2xXSr')
		for div in divs:
			self.currCondition = div.text
			break

	def weather(self):
		from datetime import datetime
		today = datetime.today().strftime('%A')
		self.speakResult = "Currently in " + self.city + ", its " + self.tempValue + " degree, with a " + self.currCondition 
		return [self.tempValue, self.currCondition, today, self.city, self.speakResult]


w = WEATHER()

def dataUpdate():
	w.updateWeather()

##### WEATHER #####
def weather():
	return w.weather()

### COVID ###

def latestNews(news=5):
	URL = 'https://indianexpress.com/latest-news/'
	result = requests.get(URL)
	src = result.content

	soup = BeautifulSoup(src, 'html.parser')

	headlineLinks = []
	headlines = []

	divs = soup.find_all('div', {'class':'title'})

	count=0
	for div in divs:
		count += 1
		if count>news:
			break
		a_tag = div.find('a')
		headlineLinks.append(a_tag.attrs['href'])
		headlines.append(a_tag.text)

	return headlines,headlineLinks

def maps(text):
	text = text.replace('maps', '')
	text = text.replace('map', '')
	text = text.replace('google', '')
	openWebsite('https://www.google.com/maps/place/'+text)

def giveDirections(startingPoint, destinationPoint):

	geolocator = Nominatim(user_agent='assistant')
	if 'current' in startingPoint:
		res = requests.get("https://ipinfo.io/")
		data = res.json()
		startinglocation = geolocator.reverse(data['loc'])
	else:
		startinglocation = geolocator.geocode(startingPoint)

	destinationlocation = geolocator.geocode(destinationPoint)
	startingPoint = startinglocation.address.replace(' ', '+')
	destinationPoint = destinationlocation.address.replace(' ', '+')

	openWebsite('https://www.google.co.in/maps/dir/'+startingPoint+'/'+destinationPoint+'/')

	startinglocationCoordinate = (startinglocation.latitude, startinglocation.longitude)
	destinationlocationCoordinate = (destinationlocation.latitude, destinationlocation.longitude)
	total_distance = great_circle(startinglocationCoordinate, destinationlocationCoordinate).km #.mile
	return str(round(total_distance, 2)) + 'KM'

def openWebsite(url='https://www.google.com/'):
	webbrowser.open(url)

def jokes():
	URL = 'https://icanhazdadjoke.com/'
	result = requests.get(URL)
	src = result.content

	soup = BeautifulSoup(src, 'html.parser')

	try:
		p = soup.find('p')
		return p.text
	except Exception as e:
		raise e


def youtube(query):
	query = query.replace('play',' ')
	query = query.replace('on youtube',' ')
	query = query.replace('youtube',' ')

	print("Searching for videos...")
	from youtubesearchpython import VideosSearch
	videosSearch = VideosSearch(query, limit = 1)
	results = videosSearch.result()['result']
	print("Finished searching!")
	webbrowser.open('https://www.youtube.com/watch?v=' + results[0]['id'])
	return "Enjoy..."


def googleSearch(query):
	if 'image' in query:
		query += "&tbm=isch"
	query = query.replace('images','')
	query = query.replace('image','')
	query = query.replace('search','')
	query = query.replace('show','')
	webbrowser.open("https://www.google.com/search?q=" + query)
	return "Here you go..."

def sendWhatsapp(phone_no='',message=''):
	phone_no = '+91' + str(phone_no)
	webbrowser.open('https://web.whatsapp.com/send?phone='+phone_no+'&text='+message)
	import time
	from pynput.keyboard import Key, Controller
	time.sleep(10)
	k = Controller()
	k.press(Key.enter)

def email(rec_email=None, text="Hello, It's F.R.I.D.A.Y. here...", sub='F.R.I.D.A.Y.'):
	USERNAME = os.getenv('MAIL_USERNAME') # email address
	PASSWORD = os.getenv('MAIL_PASSWORD')
	if not USERNAME or not PASSWORD:
		raise Exception("MAIL_USERNAME or MAIL_PASSWORD are not loaded in environment, create a .env file and add these 2 values")
	
	if '@gmail.com' not in rec_email: return
	s = smtplib.SMTP('smtp.gmail.com', 587)
	s.starttls()
	s.login(USERNAME, PASSWORD)
	message = 'Subject: {}\n\n{}'.format(sub, text)
	s.sendmail(USERNAME, rec_email, message)
	print("Sent")
	s.quit()


def downloadImage(query, n=4):
	query = query.replace('images','')
	query = query.replace('image','')
	query = query.replace('search','')
	query = query.replace('show','')
	URL = "https://www.google.com/search?tbm=isch&q=" + query
	result = requests.get(URL)
	src = result.content

	soup = BeautifulSoup(src, 'html.parser')
	imgTags = soup.find_all('img', class_='yWs4tf') # old class name -> t0fcAb

	if os.path.exists('Downloads')==False:
		os.mkdir('Downloads')

	count=0
	for i in imgTags:
		if count==n: break
		try:
			urllib.request.urlretrieve(i['src'], 'Downloads/' + str(count) + '.jpg')
			count+=1
			print('Downloaded', count)
		except Exception as e:
			raise e

