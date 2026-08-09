from services.card_profile_service import CardProfileService

service = CardProfileService()


result = service.add_reference("my_first_card", "scans/last_card.jpg")


print("DODANO REFERENCJĘ:")


print(result)
