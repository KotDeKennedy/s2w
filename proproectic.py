
# coding=windows-1251
import speech_recognition as sr
import cv2
import numpy as np
from PIL import Image
import pytesseract
import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv

# sampling rate
freq = 44100    # recom 44100 

# recording time
duration = int(input("Duration: "))

# duration and sampling rate
recording = sd.rec(int(duration * freq), 
                   samplerate=freq, channels=2)

# time
sd.wait()

print("\nEnd\n")

# recorded 2 file
wv.write("recording.wav", recording, freq, sampwidth=2)

class CommunicationAssistant:
    def __init__(self):
        self.speech_recognizer = sr.Recognizer()
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def recognize_speech(self, audio_file):
        try:
            with sr.AudioFile(audio_file) as source:
                audio = self.speech_recognizer.record(source)
            
            text = self.speech_recognizer.recognize_google(audio, language="ru-RU")
            return text
        except Exception as e:
            print(f"Ошибка при распознавании речи: {e}")
            return None

    def recognize_gestures(self, video_path):
        cap = cv2.VideoCapture(video_path)
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
            
            for (x, y, w, h) in faces:
                roi = gray[y:y+h, x:x+w]
                text = pytesseract.image_to_string(roi, lang='rus')
                
                if text:
                    cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            
            cv2.imshow('Gestures', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()

# calling a class
assistant = CommunicationAssistant()

# speech 2 word
speech_result = assistant.recognize_speech(r"C:\Users\kot72\source\repos\proproectic\proproectic\recording.wav")
print(f"Распознанная речь: {speech_result}")

# image 2 word
assistant.recognize_gestures("\address\fill.bruh")

# So... .