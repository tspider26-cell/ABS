from services.card_library_service import CardLibraryService

library = CardLibraryService()


result = library.add_card("scans/last_card.jpg", "my_first_card")


print("\nWYNIK DODANIA:")
print(result)
