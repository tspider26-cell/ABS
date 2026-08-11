from services.tcgdex_image_database_builder import TCGdexImageDatabaseBuilder


print("=" * 40)
print("ABS TCGDEX IMAGE DATABASE BUILDER v1.0")
print("=" * 40)


builder = TCGdexImageDatabaseBuilder()


results = builder.build_test_database()


print()
print("TOTAL:")
print(len(results))


print("=" * 40)
