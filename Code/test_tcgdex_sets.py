# ABS TCGDEX SET DIAGNOSTIC v1.0
# Search real TCGdex set IDs

import requests


def search_sets():

    print("=" * 40)
    print("ABS TCGDEX SET SEARCH")
    print("=" * 40)

    url = "https://api.tcgdex.net/v2/en/sets"

    try:

        response = requests.get(
            url,
            timeout=30
        )

        print("HTTP:", response.status_code)

        if response.status_code != 200:
            print(response.text)
            return


        sets = response.json()

        print("TOTAL SETS:", len(sets))
        print()

        keywords = [
            "perfect",
            "order",
            "mega",
            "me03",
            "por"
        ]


        found = 0


        for item in sets:

            text = (
                str(item.get("id", "")) +
                " " +
                str(item.get("name", ""))
            ).lower()


            if any(
                key in text
                for key in keywords
            ):

                print(
                    {
                        "id": item.get("id"),
                        "name": item.get("name"),
                        "logo": item.get("logo")
                    }
                )

                found += 1


        print()
        print("FOUND:", found)


    except Exception as e:

        print("ERROR:", e)



if __name__ == "__main__":
    search_sets()
