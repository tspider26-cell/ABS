from recognition.feature_matcher_v21 import FeatureMatcherV21

matcher = FeatureMatcherV21()


results = matcher.find_best("scans/last_card.jpg", "database/images")


print("\nMATCHER V2.1:")


for item in results:

    print(item)
