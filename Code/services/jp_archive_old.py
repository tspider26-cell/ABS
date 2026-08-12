import os
import shutil

SOURCE = r"D:\ABS_DATA\POKEMON\TCG\JP"
ARCHIVE = r"D:\ABS_DATA\POKEMON\TCG\JP_ARCHIVE_OLD"


def main():

    moved = 0
    skipped = 0

    os.makedirs(ARCHIVE, exist_ok=True)

    for root, dirs, files in os.walk(SOURCE):

        for file in files:

            # zostawiamy nowe pliki
            if file.startswith("JP-"):
                continue

            src = os.path.join(root, file)

            rel = os.path.relpath(src, SOURCE)

            dst = os.path.join(ARCHIVE, rel)

            os.makedirs(os.path.dirname(dst), exist_ok=True)

            if os.path.exists(dst):
                skipped += 1
                continue

            shutil.move(src, dst)

            moved += 1

            if moved % 500 == 0:
                print("MOVED:", moved)

    print("=" * 50)
    print("ARCHIVE COMPLETE")
    print({"moved": moved, "skipped": skipped})


if __name__ == "__main__":
    main()
