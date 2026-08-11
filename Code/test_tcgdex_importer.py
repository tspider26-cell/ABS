from services.tcgdex_importer import TCGdexImporter

importer = TCGdexImporter("database/sources/tcgdex/cards.json")


cards = importer.import_cards()


print("=" * 40)
print("ABS TCGDEX IMPORTER v1.0")
print("=" * 40)

print()

print({"imported": len(cards)})

print()

if cards:
    print(cards[0])

print()

print("=" * 40)
