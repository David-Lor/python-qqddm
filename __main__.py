import datetime
import sys

import qqddm.main


if __name__ == '__main__':
    picture_filename = sys.argv[-1]
    with open(picture_filename, "rb") as f:
        picture_bytes = f.read()

        converter = qqddm.main.AnimeConverter(
            generate_proxy="socks5://server.lan:9053",
        )
        result = converter.convert(picture_bytes)

        print("Result:", [str(url) for url in result.pictures_urls])

        pictures = converter.download(result)

        now_isoformat = datetime.datetime.now().isoformat()
        for i, pic in enumerate(pictures):
            extension = "png" if i == 0 else "jpg"
            filepath = f"/media/ram/qqddm_{now_isoformat}_{i}.{extension}"
            with open(filepath, "wb") as f:
                f.write(pic)
