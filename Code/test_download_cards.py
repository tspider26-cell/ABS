from services.tcgdex_service import TCGdexService
from services.tcg_image_database import TCGImageDatabase

cards = [
    "base1-1",
    "base1-2",
    "base1-3",
    "base1-4",
    "base1-5",
]


tcgdex = TCGdexService()

images = TCGImageDatabase()


for card_id in cards:

    print("\nPOBIERAM:", card_id)

    card = tcgdex.get_card(card_id, "en")

    if card is None:

        print("BRAK KARTY")

        continue

    info = tcgdex.get_card_info(card)

    print(info["name"])

    images.download_card_image(card_id, info["image"])
