from pathlib import Path
import json


class PTCGCardProfileService:

    def __init__(
        self,
        cards_file=r"D:\PTCG_FULL_DATABASE\database\cards.json",
        artists_file=r"D:\PTCG_FULL_DATABASE\database\artists.json",
        image_index_file=r"D:\PTCG_FULL_DATABASE\database\image_master_index_ranked_v2.json",
        slug_file=r"C:\ABS\Code\serebii_slug_database_v1.json",
    ):

        self.cards_file = Path(cards_file)
        self.artists_file = Path(artists_file)
        self.image_index_file = Path(image_index_file)
        self.slug_file = Path(slug_file)

        self.cards = []
        self.artists = []
        self.image_index = {}
        self.slugs = {}

        self.load()

    def load(self):

        with open(self.cards_file, "r", encoding="utf-8") as file:
            self.cards = json.load(file)

        with open(self.artists_file, "r", encoding="utf-8") as file:
            self.artists = json.load(file)

        with open(self.image_index_file, "r", encoding="utf-8") as file:

            data = json.load(file)

            self.image_index = data.get("cards", {})

        if self.slug_file.exists():

            with open(self.slug_file, "r", encoding="utf-8") as file:

                self.slugs = json.load(file)

    def statistics(self):

        return {
            "cards": len(self.cards),
            "artists": len(self.artists),
            "image_keys": len(self.image_index),
            "set_slugs": len(self.slugs),
        }

    def find_card(self, card_id):

        for card in self.cards:

            if card.get("card_id") == card_id:

                return card

        return None

    def find_artist(self, artist_name):

        if not artist_name:

            return None

        for artist in self.artists:

            if artist.get("name") == artist_name:

                return artist

        return None

    def get_image_keys(self, card):

        if not card:

            return []

        keys = []

        card_id = card.get("card_id")
        set_id = card.get("set_id")
        number = card.get("number")

        if card_id:

            keys.append(card_id)

        if set_id and number:

            keys.append(f"{set_id}-{number}")

        slug = self.slugs.get(set_id)

        if slug and number:

            keys.append(f"{slug}-{number}")

        return keys

    def get_images(self, card):

        if not card:

            return []

        for key in self.get_image_keys(card):

            if key in self.image_index:

                return self.image_index[key]

        return []

    def get_profile(self, card_id):

        card = self.find_card(card_id)

        if not card:

            return None

        artist = self.find_artist(card.get("artist"))

        return {
            "card": {
                "id": card.get("card_id"),
                "name": card.get("name"),
                "set_id": card.get("set_id"),
                "set_name": card.get("set_name"),
                "number": card.get("number"),
                "rarity": card.get("rarity"),
                "type": card.get("type"),
            },
            "artist": {
                "name": card.get("artist"),
                "status": ("found" if artist else "missing"),
            },
            "images": self.get_images(card),
            "source": card.get("source"),
            "source_url": card.get("source_url"),
        }
