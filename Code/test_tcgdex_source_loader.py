from services.tcgdex_source_loader import TCGdexSourceLoader


loader = TCGdexSourceLoader()


result = loader.extract()


print("=" * 40)
print("ABS TCGDEX SOURCE LOADER v1.0")
print("=" * 40)

print()

print(result)

print()

print("=" * 40)
