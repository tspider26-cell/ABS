from services.tcgdex_full_image_builder import TCGdexFullImageBuilder

print("=" * 40)
print("ABS FULL IMAGE BUILDER TEST")
print("=" * 40)


builder = TCGdexFullImageBuilder(start=266, limit=50)


builder.build()


print("=" * 40)
