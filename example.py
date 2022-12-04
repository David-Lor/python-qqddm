import datetime
import sys

import httpx

import qqddm.main
import qqddm.models.exceptions.qqddm_api


if __name__ == '__main__':
    # Start by reading the content of a picture.
    # Run this script like this:
    #    python example.py /path/to/a/picture.jpg

    picture_filename = sys.argv[-1]
    if picture_filename.startswith("http"):
        r = httpx.get(
            url=picture_filename,
            headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0"}
        )
        r.raise_for_status()
        picture_bytes = r.content
    else:
        with open(picture_filename, "rb") as f:
            picture_bytes = f.read()

    # Initialize the AnimeConverter class. Optional settings can be used for customizing the requesting behaviour.
    converter = qqddm.main.AnimeConverter()

    # Result is returned as an `AnimeResult` object
    try:
        result = converter.convert(picture_bytes)
    except qqddm.models.exceptions.qqddm_api.IllegalPictureQQDDMApiResponseException:
        # The API may forbid converting images with sensible content
        print("The image provided is forbidden, try with another picture")
        exit(1)
    except qqddm.models.exceptions.qqddm_api.InvalidQQDDMApiResponseException as ex:
        # If the API returned any other error, show the response body
        print(f"API returned error; response body: {ex.response_body}")
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
        extension = "png" if i == 0 else "jpg"
        filepath = f"qqddm_{now_isoformat}_{i}.{extension}"
        with open(filepath, "wb") as f:
            f.write(pic)
