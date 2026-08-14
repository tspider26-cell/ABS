from pathlib import Path
import json

INDEX = Path(r"D:\PTCG_FULL_DATABASE\database\image_master_index_ranked_v2.json")

OUTPUT = Path(r"D:\PTCG_FULL_DATABASE\logs\preferred_image_path_audit_v1.json")


def main():

    print("=" * 70)
    print("ABS DATABASE v2")
    print("PREFERRED IMAGE PATH AUDIT v1")
    print("=" * 70)

    with open(INDEX, "r", encoding="utf-8") as f:
        data = json.load(f)

    missing = []
    total = 0
    ok = 0

    for card_id, images in data["cards"].items():

        for img in images:

            if img.get("preferred"):

                total += 1

                file = img.get("file")

                if file and Path(file).exists():

                    ok += 1

                else:

                    missing.append(
                        {"card": card_id, "file": file, "source": img.get("source")}
                    )

    report = {
        "preferred_images": total,
        "existing": ok,
        "missing": len(missing),
        "missing_files": missing[:500],
    }

    with open(OUTPUT, "w", encoding="utf-8") as f:

        json.dump(report, f, indent=2, ensure_ascii=False)

    print()
    print("PREFERRED:", total)
    print("EXISTING:", ok)
    print("MISSING:", len(missing))

    print()
    print("OUTPUT:")
    print(OUTPUT)

    print("=" * 70)


if __name__ == "__main__":
    main()
