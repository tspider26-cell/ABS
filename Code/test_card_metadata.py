from services.card_metadata_service import CardMetadataService


IMAGE = "scans/archive/card_0005.jpg"


service = CardMetadataService()

result = service.analyze(
    IMAGE
)


print("=" * 40)
print("ABS CARD METADATA SERVICE v1.4")
print("=" * 40)

print()

print(result)

print()

print("=" * 40)
