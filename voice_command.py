from subprocess import call
import speech_recognition as sr
import serial
import RPi.GPIO as GPIO      
import os, time
import Adafruit_DHT
from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD
from datetime import datetime
from datetime import date

r= sr.Recognizer()
led=4
text = {}
text1 = {}
lampa_upaljena=0
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(led, GPIO.OUT)
lcd = LCD()
def safe_exit(signum, frame):
    exit(1)
def ispis(fname):
    signal(SIGTERM, safe_exit)
    signal(SIGHUP, safe_exit)
    lcd.text("SURV Projekat", 1)
    lcd.text(fname, 2)
  
def listen1():
    with sr.Microphone(device_index = 2) as source:
               r.adjust_for_ambient_noise(source)
               print("Komanda:")
               ispis("Komanda:")
               audio = r.listen(source)
               print("Procesuiram...")
               ispis("Procesuiram:")
    return audio
def voice(audio1):
       try: 
         text1 = r.recognize_google(audio1,language="bs-BA") 
         print ("Rekli ste: " + text1);
         return text1; 
       except sr.RequestError as e: 
          print("Ne mogu dobiti rezultat")
          return 0
def main(text):
       audio1 = listen1() 
       text = voice(audio1);
       lcd.clear()
       global lampa_upaljena
       if 'lamp' in text:
           if lampa_upaljena==0 :
               ispis("Palim lampu:")
               GPIO.output(led , 1)
               lampa_upaljena=1
               call(["espeak", "-s130 -veurope/bs" , "Palim lampu"])
           else:
               ispis("Gasim lampu:")
               GPIO.output(led , 0)
               lampa_upaljena=0
               call(["espeak", "-s130 -veurope/bs" , "Gasim lampu"])
       elif 'temp' in text:
        humidity,temperature =Adafruit_DHT.read(Adafruit_DHT.DHT11, 27)
        if humidity is not None and temperature is not None:
            text2="Temp: {0:0.1f}C".format(temperature);
            lcd.text(text2,1)
            text3="Vlaznost: {0:0.1f}%".format(humidity);
            lcd.text(text3,2)
        else:
              call(["espeak", "-s130 -veurope/bs" , "Ne dobijam vrijednosti senzora temperature"])
              lcd.text("Nema podataka",1)
       elif 'zatvori' in text:
          ispis("Zatvaram...")
          lcd.clear()
          os._exit(0);
       elif 'vrijeme' in text:
          now=datetime.now()
          curr_t=now.strftime("%H:%M:%S");
          ispis(curr_t)
       elif 'datum' in text:
          now=date.today()
          curr_t=now.strftime("%d.%m.%Y");
          ispis(curr_t)
       else:
          call(["espeak", "-s130 -veurope/bs" , "Nepoznata komanda"])
       text = {} 
if __name__ == '__main__':
 GPIO.output(led , 0)
 lampa_upaljena=0
 while(1):
         text = {}
         call(["espeak", "-s130 -veurope/bs" ," Čekam vašu komandu"])
         main(text)