from services.tcgdex_sync import TCGdexSync


sync = TCGdexSync()

result = sync.build_cards_file()


print("=" * 40)
print("ABS TCGDEX SYNC v1.1")
print("=" * 40)

print()

print(result)

print()

print("=" * 40)
