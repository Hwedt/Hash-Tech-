import json
import requests
import time

telegram_bot_id = "bot1519053190:AAFG5pVxFcvrwmA9sp0rUuRXYf4aJdWvAKk"

city = input("Enter name of your city ")
chat_id = input("Enter your chat id ")
telegram_chat_id = chat_id
def aqi_check():

	url = "https://api.waqi.info/feed/{}/?token=be18f4ea15181eacf02c1d17b008adfd23dd0715".format(city)
	response = requests.get(url)
	data = response.json()
	current_aqi = data['data']['aqi']
	city_name = data['data']['city']['name']
	status = data['status']
	return current_aqi,city_name,status;

def send_telegram_alert(message,chat_id):
	url = "https://api.telegram.org/" + telegram_bot_id + "/sendMessage"
	data = {
		"chat_id": chat_id,
		"text": message
	}
	try:
		response = requests.request("POST",url,params = data)
		print("This is the telegram url")
		print(url)
		print("This is the telegram response")
		print(response.text)
		telegram_data = json.loads(response.text)
		return telegram_data["ok"]
	except Exception as e:
		print("An error occurred in sending the alert message via Telegram")
		print(e)
		return False

while True:
	aqi,city,status = aqi_check()
	if status != "ok":
		print("Response was unscessful")
		continue
	if (aqi >= 0 and aqi <= 50):
		message = f"Current Air Quality Index is {aqi} in {city}\nAir Quality is considered satisfactory"
		print(message)
		send_telegram_alert(message,chat_id)
	elif (aqi >= 51 and aqi <= 100):
		message = f"Warning! Air Quality Index is {aqi} in {city}\nAir Quality is acceptable; However, for some reason there may be a moderate health concern"
		print(message)
		send_telegram_alert(message,chat_id)
	elif (aqi >= 101 and aqi <= 150):
		message = f"Warning! Air Quality Index is {aqi} in {city}\nMembers of sensitve groups may experience health effects"
		print(message)
		send_telegram_alert(message,chat_id)
	elif (aqi >= 151 and aqi <= 200):
		message = f"Warning! Air Quality Index is {aqi} in {city}\nEveryone may begin to experience health effects."
		print(message)
		send_telegram_alert(message,chat_id)
	elif (aqi >= 201 and aqi <= 300):
		message = f"Warning! Air Quality Index is {aqi} in {city}\nHealth alert! Everyone may experience more serious health effects."
		print(message)
		send_telegram_alert(message,chat_id)
	elif (aqi >= 301 and aqi <= 500):
		message = f"Warning! Air Quality Index is {aqi} in {city}\nEmergency! The entire population is more likely to be affected."
		print(message)
		send_telegram_alert(message,chat_id)
	time.sleep(900)

