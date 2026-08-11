from services.card_database_service import CardDatabaseService


metadata = {

    "family": "Pokemon",
    "number": "035/088"

}


service = CardDatabaseService(
    "database/cards.json"
)


result = service.find(
    metadata
)


print("=" * 40)
print("ABS CARD DATABASE SERVICE v1.0")
print("=" * 40)

print()

print(result)

print()

print("=" * 40)
