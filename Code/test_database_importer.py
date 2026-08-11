from services.database_importer import DatabaseImporter

cards = [
    {
        "id": "por-035-088",
        "name": "Spritzee",
        "set": "Perfect Order",
        "code": "POR",
        "number": "035/088",
        "languages": ["EN"],
        "rarity": "Common",
        "images": [],
        "sources": ["manual"],
    }
]


importer = DatabaseImporter("database/master_cards.json")


result = importer.import_cards(cards)


print("=" * 40)
print("ABS DATABASE IMPORTER v1.0")
print("=" * 40)

print()

print(result)

print()

print("=" * 40)
