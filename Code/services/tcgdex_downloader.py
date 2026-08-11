# ABS TCGdex Downloader v2.0
# Downloads TCGdex archive for ABS database

import urllib.request
from pathlib import Path


class TCGdexDownloaderV2:

    def __init__(
        self,
        url="",
        output="database/downloads/tcgdex.zip"
    ):

        self.url = url
        self.output = Path(output)


    def download(self):

        if not self.url:

            return {
                "downloaded": False,
                "message": "Brak adresu źródła TCGdex"
            }


        try:

            self.output.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            urllib.request.urlretrieve(
                self.url,
                self.output
            )

            size = self.output.stat().st_size

            return {
                "downloaded": True,
                "file": str(self.output),
                "size": size
            }


        except Exception as e:

            return {
                "downloaded": False,
                "error": str(e)
            }
