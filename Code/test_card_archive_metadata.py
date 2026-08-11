from services.card_archive_service import CardArchiveService

IMAGE = "scans/last_card.jpg"


archive = CardArchiveService()


result = archive.archive_card(IMAGE)


print("=" * 40)
print("ABS CARD ARCHIVE METADATA TEST v1.1")
print("=" * 40)


if result:

    print("NOWA KARTA:")

    print(result)


else:

    print("BRAK PLIKU")


print("=" * 40)
