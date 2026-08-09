from services.card_profile_service import CardProfileService

service = CardProfileService()


result = service.create_profile("my_first_card", "scans/last_card.jpg")


print("UTWORZONO PROFIL:")

print(result)
