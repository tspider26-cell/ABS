from services.recognition_service import RecognitionService

service = RecognitionService()


result = service.recognize_card("scans/last_card.jpg")


print("\nRECOGNITION SERVICE PROFILE MODE")
print("================================")

print(result)
