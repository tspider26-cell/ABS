from recognition.card_matcher import CardMatcher

matcher = CardMatcher()


score = matcher.compare("scans/last_card.jpg", "database/images/base1-1.png")


print("WYNIK:", score)
