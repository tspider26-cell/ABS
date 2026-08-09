from recognition.card_profile_matcher import CardProfileMatcher

matcher = CardProfileMatcher()


results = matcher.recognize("scans/last_card.jpg")


print("\nCARD PROFILE MATCHER:")


for item in results:

    print(item)
