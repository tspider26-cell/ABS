# ABS TCGdex Full Image Builder v4.2
# File prepared for:
# C:\ABS\Code\services\tcgdex_full_image_builder.py

import argparse

class TCGdexFullImageBuilder:
    def __init__(self, start=0, limit=500, workers=16):
        self.start = start
        self.limit = limit
        self.workers = workers

    def build(self):
        print("ABS TCGdex Full Image Builder v4.2")
        print(f"start={self.start} limit={self.limit} workers={self.workers}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--limit", type=int, default=500)
    parser.add_argument("--workers", type=int, default=16)
    args = parser.parse_args()
    TCGdexFullImageBuilder(
        args.start,
        args.limit,
        args.workers
    ).build()
