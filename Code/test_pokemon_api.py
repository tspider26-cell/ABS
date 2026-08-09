from services.card_database_service import CardDatabaseService

service = CardDatabaseService()


card = service.search_card("pikachu")


if card:

    info = service.get_card_info(card)

    print("\nDANE KARTY:")
    print(info)

    image = service.download_card_image(info["image"], "pikachu.jpg")

    print("\nOBRAZ:", image)


else:

    print("Nie znaleziono karty")
