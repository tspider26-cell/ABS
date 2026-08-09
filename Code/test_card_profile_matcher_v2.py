from recognition.card_profile_matcher_v2 import CardProfileMatcherV2

matcher = CardProfileMatcherV2()


results = matcher.recognize("scans/last_card.jpg")


print("\nCARD PROFILE MATCHER V2")
print("========================")


for item in results:

    print("\nKARTA:")
    print(item["card"])

    print("PEWNOŚĆ:", item["score"])

    print("NAJLEPSZA REFERENCJA:", item["best_reference"])

    print("\nREFERENCJE:")

    for ref in item["references"]:

        print(ref)
