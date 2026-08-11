from services.card_database_service_v2 import CardDatabaseService


print("=" * 40)
print("ABS CARD DATABASE SERVICE v2.0")
print("=" * 40)


db = CardDatabaseService()


print()
print("DATABASE:")
print(db.stats())


print()
print("TEST ID me03-035:")

card = db.find_by_id("me03-035")
print(card)


print()
print("TEST SET + NUMBER:")

card = db.find_by_set_number(
    "me03",
    "035/088"
)

print(card)


print()
print("TEST NAME:")

results = db.search_name("Spritzee")

print(results[:3])


print("=" * 40)
