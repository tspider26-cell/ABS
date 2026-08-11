# ABS TCGDEX SET CARDS DIAGNOSTIC v1.0
# Inspect the real card IDs used by TCGdex for Perfect Order (me03)

import requests


def inspect_set():

    print("=" * 40)
    print("ABS TCGDEX SET CARDS")
    print("=" * 40)

    set_id = "me03"

    url = f"https://api.tcgdex.net/v2/en/sets/{set_id}"

    try:

        response = requests.get(
            url,
            timeout=30
        )

        print("HTTP:", response.status_code)

        if response.status_code != 200:
            print(response.text)
            return

        data = response.json()

        print()
        print("SET:")
        print({
            "id": data.get("id"),
            "name": data.get("name"),
            "card_count": data.get("cardCount")
        })

        print()
        print("CARDS:")

        cards = data.get("cards", [])

        print("TOTAL:", len(cards))
        print()

        # Show first cards and specifically card 35
        for card in cards[:10]:

            print({
                "id": card.get("id"),
                "localId": card.get("localId"),
                "name": card.get("name")
            })

        print()
        print("SEARCHING LOCAL ID 35...")
        print()

        matches = []

        for card in cards:

            if str(card.get("localId")) in ("35", "035"):

                matches.append({
                    "id": card.get("id"),
                    "localId": card.get("localId"),
                    "name": card.get("name")
                })

        if matches:

            for match in matches:
                print(match)

        else:

            print("NO CARD WITH LOCAL ID 35 FOUND")


    except Exception as e:

        print("ERROR:", e)


if __name__ == "__main__":
    inspect_set()
