from services.tcgdex_full_importer import TCGdexFullImporter

print("=" * 40)
print("ABS TCGDEX FULL IMPORT TEST v1.0")
print("=" * 40)

importer = TCGdexFullImporter()

result = importer.import_database()

print()
print(result)

print("=" * 40)
