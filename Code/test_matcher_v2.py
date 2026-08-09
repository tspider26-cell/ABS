from recognition.card_matcher import CardMatcher

matcher = CardMatcher()


result = matcher.find_best_match("scans/last_card.jpg", "database/images")


print("\nWYNIK KOŃCOWY:")

print(result)
