from services.card_profile_service import CardProfileService

service = CardProfileService()


result = service.capture_reference("my_first_card", "scans/last_card.jpg")


print("\nCAPTURE REFERENCE:")
print(result)
