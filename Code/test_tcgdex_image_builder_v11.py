from services.tcgdex_image_database_builder_v11 import (
    TCGdexImageDatabaseBuilderV11,
)


print("=" * 40)
print("ABS TCGDEX IMAGE BUILDER v1.1 TEST")
print("=" * 40)

builder = TCGdexImageDatabaseBuilderV11(
    batch_size=100
)

result = builder.build()

print()
print("TEST FINISHED")
print(result["stats"])
print("=" * 40)
