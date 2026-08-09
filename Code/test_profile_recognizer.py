from recognition.profile_recognizer import ProfileRecognizer

recognizer = ProfileRecognizer()


result = recognizer.recognize("scans/last_card.jpg")


print("\nPROFILE RECOGNIZER:")
print("===================")


print(result)
