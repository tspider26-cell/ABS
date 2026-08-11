from services.card_metadata_integration_service import CardMetadataIntegrationService

IMAGE = "scans/archive/card_0005.jpg"


service = CardMetadataIntegrationService()


result = service.update_metadata(IMAGE)


print("=" * 40)
print("ABS CARD METADATA INTEGRATION v1.0")
print("=" * 40)

print()

print(result)

print()

print("=" * 40)
