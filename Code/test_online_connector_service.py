from services.online_connector_service import OnlineConnectorService


card = {

    "family": "Pokemon",
    "name": "Spritzee",
    "set": "Perfect Order",
    "code": "POR",
    "number": "035/088",
    "rarity": "Common",
    "language": "EN"

}


service = OnlineConnectorService()

result = service.search_card(
    card
)


print("=" * 40)
print("ABS ONLINE CONNECTOR SERVICE v1.0")
print("=" * 40)

print()

print(result)

print()

print("=" * 40)
