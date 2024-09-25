import requests
from gtts import gTTS
import speech_recognition as sr
import pygame
import os
import time
import pyautogui

BOT_TOKEN = os.environ.get('BOT_TOKEN')
GROUP_CHAT_ID = os.environ.get('GROUP_CHAT_ID')
API_URL = f'https://api.telegram.org/bot{BOT_TOKEN}'


def get_name():
    if os.path.isfile("name.txt"):
        with open("name.txt", "r") as f:
            if not ("sorry" in f.read()):
                name = f.read()

    else:
        say("Please say your name sir")
        name = takeCommand()
        if "sorry" in name:
            while "sorry" in name:
                say("I couldnt get your name please repeat")
                name = takeCommand()
        else:
            with open("name.txt", "w") as f:
                f.write(name)
    return name

def take_screenshot_with_delay():
    # Check if the command is "Record" (case-insensitive)
    print("Recording will start in 3 seconds...")

    # Add a 5-second delay before taking the screenshot
    time.sleep(3)

    # Create a timestamped filename for the screenshot
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    screenshot_filename = f"screenshot_{timestamp}.png"

    screenshot = pyautogui.screenshot()
    screenshot.save(screenshot_filename)

    print(f"Screenshot saved as {screenshot_filename}")
    return screenshot_filename


def ocr_space_api(image_path):
    api_key = os.environ.get('OCR_API_KEY')
    api_url = 'https://api.ocr.space/parse/image'

    with open(image_path, 'rb') as image_file:
        payload = {'apikey': api_key}
        files = {'file': image_file}
        response = requests.post(api_url, data=payload, files=files)
        result = response.json()

    if result.get('ParsedResults'):
        return result['ParsedResults'][0]['ParsedText']
    else:
        return "Error or no text found"

def send_telegram_message(message):
    payload = {
        'chat_id': GROUP_CHAT_ID,
        'text': message
    }
    response = requests.post(f'{API_URL}/sendMessage', data=payload)
    return response.json()


def send_telegram_image(image_path,count):

    payload = {
        'chat_id': GROUP_CHAT_ID,
        'caption': count
    }

    # Open the image file in binary mode
    with open(image_path, 'rb') as image_file:
        files = {
            'photo': image_file
        }

        # Send a POST request to Telegram's sendPhoto API
        response = requests.post(f'{API_URL}/sendPhoto', data=payload, files=files)

    return response.json()

def activate_cheats():
    count=0

    while True:
        command = takeCommand()
        if command.lower() == "stop cheats".lower():
            break
        else:
            file_name = take_screenshot_with_delay()
            message=ocr_space_api(file_name)
            count += 1
            message = f'Question no {count} {message}give only the correct answer no explanation'
            send_telegram_message(message)
            send_telegram_image(file_name,count)
            os.remove(file_name)

def say(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    filename = "temp_audio.mp3"
    tts.save(filename)

    pygame.mixer.init()

    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.quit()
    os.remove(filename)

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        # print("Listening...")
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-IN")
            print(f"User said: {query}")
            return query
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return "Sorry, I did not understand that."
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return "Sorry, there was an issue with the speech recognition service."



def screen2text():
    name = get_name()
    print('Welcome to Screen2Text A.I')
    say(f" hi {name} how are you i am Screen2Text A.I")
    while True:
        print("Listening...")
        query = takeCommand()
        if "activate cheats".lower() in query.lower():
            activate_cheats()
        elif "stop listening".lower() in query.lower() or "shut up".lower() in query.lower():
            say(f"Okay {name}, waiting for your command.")
            while True:
                print("Waiting ...")
                query = takeCommand()
                print(f"Received query during while waiting")
                if "start".lower() in query.lower():
                    say(f"Starting, {name}.")
                    break
        else:
            say("I'm not sure what you mean. Please try again.")