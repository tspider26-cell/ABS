from recognition.auto_recognizer import AutoRecognizer

IMAGE = "database/images/my_first_card.jpg"


recognizer = AutoRecognizer()


result = recognizer.recognize(IMAGE)


print("\nSAMOROZPOZNANIE:")
print(result)


print("\nTOP 5:")

for item in result["all_results"][:5]:

    print(item)
