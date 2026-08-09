from recognition.auto_recognizer import AutoRecognizer

IMAGE = "scans/last_card.jpg"


recognizer = AutoRecognizer()


result = recognizer.recognize(IMAGE)


print("\nROZPOZNANIE KARTY:")
print(result)


print("\nTOP 5:")

for item in result["all_results"][:5]:

    print(item)
