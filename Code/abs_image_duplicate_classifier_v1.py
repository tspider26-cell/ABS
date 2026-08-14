from pathlib import Path
import json
from collections import defaultdict

BASE = Path(r"D:\PTCG_FULL_DATABASE")

DUP_FILE = BASE / "logs" / "image_duplicates_v1.json"
OUT = BASE / "logs" / "duplicate_classification_v1.json"


def classify(files):

    result = {"type": None, "files": files, "sources": []}

    for f in files:

        if "\\serebii\\english\\" in f.lower():
            result["sources"].append("SEREBII_EN")

        elif "\\serebii\\japanese\\" in f.lower():
            result["sources"].append("SEREBII_JP")

        elif "\\abs_data\\" in f.lower():
            result["sources"].append("ABS_DATA")

        else:
            result["sources"].append("OTHER")

    sources = set(result["sources"])

    if "SEREBII_EN" in sources and "SEREBII_JP" in sources:
        result["type"] = "EXACT_MULTI_LANGUAGE"

    elif len(files) > 1:
        result["type"] = "DUPLICATE"

    else:
        result["type"] = "UNKNOWN"

    return result


def main():

    print("=" * 70)
    print("ABS DATABASE v2")
    print("IMAGE DUPLICATE CLASSIFIER v1")
    print("=" * 70)

    with open(DUP_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    output = {}

    stats = defaultdict(int)

    for h, files in data.items():

        item = classify(files)

        output[h] = item

        stats[item["type"]] += 1

    report = {
        "total_groups": len(output),
        "categories": dict(stats),
        "duplicates": output,
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print()
    print("GROUPS:", len(output))

    for k, v in stats.items():
        print(k, v)

    print()
    print("OUTPUT:")
    print(OUT)
    print("=" * 70)


if __name__ == "__main__":
    main()
