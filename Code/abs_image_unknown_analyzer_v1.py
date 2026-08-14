from pathlib import Path
import json
from collections import Counter, defaultdict

INPUT = Path(r"D:\PTCG_FULL_DATABASE\logs\abs_image_inventory_v1.json")

OUTPUT = Path(r"D:\PTCG_FULL_DATABASE\logs\abs_image_unknown_report_v1.json")


def classify_unknown(path):

    p = path.lower()

    result = {"category": "OTHER", "path": path}

    if "serebii" in p:

        if "\\images\\serebii\\" in p:

            parts = p.split("\\images\\serebii\\")

            if len(parts) > 1:
                after = parts[1]

                first = after.split("\\")[0]

                if first not in ("english", "japanese"):
                    result["category"] = "SEREBII_ROOT"
                else:
                    result["category"] = "SEREBII_OTHER"

    elif "abs_data" in p:
        result["category"] = "ABS_DATA"

    return result


def main():

    print("=" * 70)
    print("ABS DATABASE v2")
    print("IMAGE UNKNOWN ANALYZER v1")
    print("=" * 70)

    with open(INPUT, "r", encoding="utf-8") as f:
        data = json.load(f)

    counter = Counter()
    examples = defaultdict(list)

    unknown_total = 0

    for img in data["images"]:

        path = img["file"]

        p = path.lower()

        is_unknown = (
            "\\english\\" not in p
            and "\\japanese\\" not in p
            and "zh" not in p
            and "tw" not in p
        )

        if is_unknown:

            unknown_total += 1

            info = classify_unknown(path)

            cat = info["category"]

            counter[cat] += 1

            if len(examples[cat]) < 10:
                examples[cat].append(path)

    report = {
        "unknown_total": unknown_total,
        "categories": dict(counter),
        "examples": dict(examples),
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4, ensure_ascii=False)

    print()
    print("UNKNOWN:", unknown_total)

    print()
    print("CATEGORIES:")

    for k, v in counter.items():
        print(f"{k}: {v}")

    print()
    print("OUTPUT:")
    print(OUTPUT)

    print("=" * 70)


if __name__ == "__main__":
    main()
