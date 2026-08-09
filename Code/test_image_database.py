from services.tcg_image_database import TCGImageDatabase

db = TCGImageDatabase()


image = db.download_card_image("base1-1", "https://assets.tcgdex.net/en/base/base1/1")


print("WYNIK:", image)
