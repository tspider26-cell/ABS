from services.card_family_service import CardFamilyService

IMAGE = "scans/archive/card_0005.jpg"


service = CardFamilyService()


result = service.analyze_card(IMAGE)


print("=" * 40)
print("ABS CARD FAMILY SERVICE TEST v1.0")
print("=" * 40)


print()

print(result)


print()

print("=" * 40)
