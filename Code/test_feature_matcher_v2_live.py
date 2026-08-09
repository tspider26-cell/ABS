from recognition.feature_matcher_v2 import FeatureMatcherV2

matcher = FeatureMatcherV2()


results = matcher.find_best("scans/last_card.jpg", "database/images")


print("\nNOWY MATCHER V2:")


for item in results:

    print(item)
