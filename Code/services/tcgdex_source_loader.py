# ABS TCGdex Source Loader v1.0
# Prepares TCGdex source folder for ABS

from pathlib import Path
import shutil
import zipfile


class TCGdexSourceLoader:

    def __init__(
        self,
        source="database/downloads/tcgdex.zip",
        target="database/sources/tcgdex"
    ):

        self.source = Path(source)
        self.target = Path(target)


    def prepare_folder(self):

        self.target.mkdir(
            parents=True,
            exist_ok=True
        )


    def extract(self):

        self.prepare_folder()

        if not self.source.exists():

            return {
                "loaded": False,
                "message": "Brak pliku TCGdex zip"
            }


        with zipfile.ZipFile(
            self.source,
            "r"
        ) as archive:

            archive.extractall(
                self.target
            )


        return {
            "loaded": True,
            "source": str(self.source),
            "target": str(self.target)
        }
