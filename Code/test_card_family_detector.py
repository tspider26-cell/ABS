from services.card_family_detector import CardFamilyDetector

IMAGE = "scans/last_card.jpg"


detector = CardFamilyDetector()


result = detector.detect(IMAGE)


print("=" * 40)
print("ABS CARD FAMILY DETECTOR v1.0")
print("=" * 40)


print()

print("RESULT:")

print(result)


print()

print("=" * 40)
