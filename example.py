import datetime
import sys
import os

import httpx
from qqddm import AnimeConverter, InvalidQQDDMApiResponseException, IllegalPictureQQDDMApiResponseException


PROXY = os.getenv("PROXY", None)
USERAGENT = os.getenv("USERAGENT", "Mozilla/5.0 (X11; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0")


if __name__ == '__main__':
    # Start by reading the content of a picture.
    # Run this script like this:
    #    python example.py /path/to/a/picture.jpg

    picture_filename = sys.argv[-1]
    if picture_filename.startswith("http"):
        r = httpx.get(
            url=picture_filename,
            headers={"User-Agent": USERAGENT}
        )
        r.raise_for_status()
        picture_bytes = r.content
    else:
        with open(picture_filename, "rb") as f:
            picture_bytes = f.read()

    # Initialize the AnimeConverter class. Optional settings can be used for customizing the requesting behaviour.
    converter = AnimeConverter(
        global_useragents=[USERAGENT],
        generate_proxy=PROXY,
    )

    # Result is returned as an `AnimeResult` object
    try:
        result = converter.convert(picture_bytes)
    except IllegalPictureQQDDMApiResponseException:
        # The API may forbid converting images with sensible content
        print("The image provided is forbidden, try with another picture")
        exit(1)
    except InvalidQQDDMApiResponseException as ex:
        # If the API returned any other error, show the response body
        print(f"API returned error ({ex}); response body: {ex.response_body}")
        exit(1)

    # noinspection PyUnboundLocalVariable
    print("Result:", result)
    print("Result URLs:", [str(url) for url in result.pictures_urls])

    # This method downloads all the pictures from the given `AnimeResult` object, simultaneously.
    # Returns a list of bytes, where each item is the picture data from each one of `result.pictures_urls`.
    pictures = converter.download(result)

    # Finally, save each returned picture.
    now_isoformat = datetime.datetime.now().isoformat()
    for i, pic in enumerate(pictures):
        filepath = f"qqddm_{now_isoformat}_{i}.jpg"
        with open(filepath, "wb") as f:
            f.write(pic)
