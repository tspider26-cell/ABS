from recognition.hybrid_matcher import HybridMatcher

matcher = HybridMatcher()


results = matcher.find_best("scans/last_card.jpg", "database/images")


print("\nHYBRID MATCHER V1:")


for item in results:

    print(item)
