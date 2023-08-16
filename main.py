import time
import requests
from characterai import PyCAI
import gtts
import vlc
import speech_recognition as sr

headers = {
  "Accept": "audio/mpeg",
  "Content-Type": "application/json",
  "xi-api-key": "ea43e5e6ecebcbc208c5080bd4b3aad6"
}
Vheaders = {
  "Accept": "application/json",
  "xi-api-key": "ea43e5e6ecebcbc208c5080bd4b3aad6"
}
DSheaders = {
  "Accept": "application/json"
}

data = {
  "text": "Hello there!",
  "model_id": "eleven_monolingual_v1",
  "voice_settings": {
    "stability": 0.75,
    "similarity_boost": 0.75
  }
}

CHUNK_SIZE = 1024

url = "https://api.elevenlabs.io/v1/text-to-speech/QkrxT5YhwdNeNIqwCGsY"
voicesUrl = "https://api.elevenlabs.io/v1/voices"
defaultSettingsUrl = "https://api.elevenlabs.io/v1/voices/settings/default"

client = PyCAI('5b5d82736c5aeb027d968351fe4201177b16bde5')
client.start()
charId = 'EEI6sjnddRIJTVC59MODiYjL0-JyDIVI2IEGLkPx2Jk'

#lain = -ArUgtiToH-xo1DBzWA7Ny8Zm6FxrF54a2s7w8Z_E2E
#jarvis = 1U5b4Nuuf3LnBLvAbaxUfllTYvttzWH2m4hjvj5ubfE

chat = client.chat.get_chat(charId)

participants = chat['participants']

if not participants[0]['is_human']:
    tgt = participants[0]['user']['username']
else:
    tgt = participants[1]['user']['username']

activateKeyword = 'activate'
deactivateKeyword = 'shut down'
deactivateScriptKeyword = 'kill script'

active = False

r = sr.Recognizer()
playing = False

def sendMessage():
    global playing
    #message = entry.get()
    message = MyText
    #entry.delete(first=0,last=999)
    data = client.chat.send_message(chat['external_id'], tgt, message, wait=True)
    #data = client.chat.send_message(charId, message, wait=True)
    print(f"{data['src_char']['participant']['name']}: {data['replies'][0]['text']}")
    charText = data['replies'][0]['text'] + ''
    mp3 = gtts.gTTS(charText, lang="en")
    mp3.save("output.mp3")
    p = vlc.MediaPlayer("output.mp3")
    p.play()
    time.sleep(1)
    while p.is_playing():
        print("playing")
        time.sleep(1)
    else:
        playing = False

def sendMessage11():
    print("Generating response...")
    global playing
    message = MyText
    reply = client.chat.send_message(charId, message, wait=True)
    data["text"] = reply['replies'][0]['text'] + " [end]"
    #print(f"{data['src_char']['participant']['name']}: {data['replies'][0]['text']}")

    response = requests.post(url, json=data, headers=headers)

    mp3 = open('output.mp3', 'wb')
    for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
        if chunk:
            mp3.write(chunk)
    mp3.close()
    p = vlc.MediaPlayer("output.mp3")
    p.play()
    time.sleep(1)
    while p.is_playing():
        print("playing")
        time.sleep(1)
    else:
        playing = False

while (1):

    print("check1")
    activated = False
    # Exception handling to handle
    # exceptions at the runtime
    try:

        # use the microphone as source for input.
        with sr.Microphone() as source2:

            # wait for a second to let the recognizer
            # adjust the energy threshold based on
            # the surrounding noise level
            r.adjust_for_ambient_noise(source2, duration=0.2)

            # listens for the user's input
            if playing is False:
                print("check2")
                print("-Listening...")
                audio2 = r.listen(source2)
                print("Writing...")

                # Using google to recognize audio
                MyText = r.recognize_google(audio2)
                MyText = MyText.lower()

                if activateKeyword in MyText:
                    active = True
                    activated = True
                if deactivateKeyword in MyText:
                    active = False
                    print("---Shutting down...")
                if deactivateScriptKeyword in MyText:
                    quit()

                if active and not activated:
                    print("User : ", MyText)
                    playing = True
                    sendMessage() #message sending
                if activated:
                    print("---Activating...")
                if not activated and not active:
                    print("Not active")

    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

    except sr.UnknownValueError:
        print("unknown error occurred")

