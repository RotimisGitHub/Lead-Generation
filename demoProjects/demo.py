import os

import pyaudio
import speech_recognition
import pyttsx3
import sounddevice as sd
import numpy as np


def _recordAudio():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/rotimi_jatto/PycharmProjects/Proper_Projects/Google_scraping/leads/service_account.json'
    sr = speech_recognition.Recognizer()

    # Parameters for recording
    duration = 5.0  # seconds
    sampling_rate = 44100  # Hertz

    audio_acquired = False
    retries = 0
    # Record audio
    while audio_acquired is False or retries != 2:
        try:

            recording = sd.rec(int(duration * sampling_rate), samplerate=sampling_rate, channels=2)
            sd.wait()
            print(recording)
            byte_data = np.int16(recording).tobytes()

            # Create an AudioData instance
            audio_data = speech_recognition.AudioData(byte_data, sampling_rate, 2)

            text = sr.recognize_google_cloud(audio_data)
            if text:
                audio_acquired = True
                print(text, "from audio input")
                return text
        except speech_recognition.RequestError as e:
            print(f"Could not Request Results: {e}")
            retries += 1

        except speech_recognition.UnknownValueError as e:
            print(f"Couldn't process Audio: {e}")
            retries += 1


_recordAudio()
