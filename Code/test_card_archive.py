from services.card_archive_service import CardArchiveService

IMAGE = "scans/last_card.jpg"


archive = CardArchiveService()


result = archive.archive_card(IMAGE)


print("=" * 40)
print("ABS CARD ARCHIVE TEST v1.0")
print("=" * 40)


if result:

    print("ZAPISANO:")

    print(result)

else:

    print("Nie znaleziono pliku")


print("=" * 40)
