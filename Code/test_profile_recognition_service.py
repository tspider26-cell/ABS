from services.profile_recognition_service import ProfileRecognitionService

service = ProfileRecognitionService()


result = service.recognize_card("scans/last_card.jpg")


print("\nPROFILE RECOGNITION SERVICE")
print("===========================")


print(result)
