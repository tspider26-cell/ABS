from services.tcgdex_service import TCGdexService

service = TCGdexService()

card = service.get_card("base1-1", "en")


if card:

    info = service.get_card_info(card)

    print("KARTA:")
    print("NAZWA:", info["name"])
    print("NUMER:", info["number"])
    print("RZADKOŚĆ:", info["rarity"])
    print("SERIA:", info["set"])
    print("OBRAZ:", info["image"])

    image = service.download_image(info["image"], "alakazam.png")

    print("PLIK:", image)


else:

    print("NIE ZNALEZIONO KARTY")
