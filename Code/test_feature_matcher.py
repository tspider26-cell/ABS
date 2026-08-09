from recognition.feature_matcher import FeatureMatcher

matcher = FeatureMatcher()


result = matcher.find_best("scans/last_card.jpg", "database/images")


print("WYNIKI:")

for card in result:

    print(card)
