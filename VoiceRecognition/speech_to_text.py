import speech_recognition as sr

def get_voice_input():
  recognizer = sr.Recognizer()
  with sr.Microphone() as source:
    print("Speak your command:")
    audio = recognizer.listen(source)
  try:
    text = recognizer.recognize_google(audio)
    print("You said: " + text)
    return text
  except sr.UnknownValueError:
    print("Could not understand audio")
    return None
