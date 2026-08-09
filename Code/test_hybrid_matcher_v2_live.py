from recognition.hybrid_matcher_v2 import HybridMatcherV2

matcher = HybridMatcherV2()


results = matcher.find_best("scans/last_card.jpg", "database/images")


print("\nHYBRID MATCHER V2:")


for item in results:

    print(item)
