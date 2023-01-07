# QQ's "Different Dimension Me" Animefier Python library

Python wrapper for [QQ's "Different Dimension Me" AI](https://h5.tu.qq.com/web/ai-2d/cartoon/index) API, that applies an anime-theme to any given picture.

## Installing

This package was developed & tested under Python 3.9. Available on [PyPI](https://pypi.org/project/qqddm):

```bash
pip install --user qqddm
```

## Usage

Check the [example](example.py) code.

### Known issues and limitations of the API

- **Only pictures with human faces**: since 2022-12-06, the QQ's API became stricter with the pictures being converted, and requires them to have a human face.
- **Forbidden images**: the QQ's API refuses to convert images with sensible or political content.

## Changelog

Versions 0.y.z are expected to be unstable, and the library API may change on Minor (y) releases.

- 0.1.1
  - Update to the new "overseas" API, which can be used from outside China
  - Fix how images are downloaded using threads
- 0.0.3
  - Add new custom exception `ParamInvalidQQDDMApiResponseException`
  - Refactor mapping of API response codes with custom exceptions, now done programatically, defining the corresponding response code on each exception class
- 0.0.2
  - Add new `x-sign` headers required by the API since 2022-12-06.
  - Add new custom exceptions based on errors returned by the API: `VolumnLimitQQDDMApiResponseException`, `AuthFailedQQDDMApiResponseException`, `NotAllowedCountryQQDDMApiResponseException`, `NoFaceInPictureQQDDMApiResponseException`.
- 0.0.1
  - Initial release:
    - Class-based interface.
    - Pass an image (as bytes) and send it to QQ API, returning the resulting images URLs.
    - Download the returned images URLs.
    - Requests settings (different for QQ API and for downloading result images): request timeouts, proxy, user-agents.
