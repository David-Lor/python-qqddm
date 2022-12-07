# QQ's "Different Dimension Me" Animefier Python library

Python wrapper for QQ's "Different Dimension Me" AI, that applies an anime-theme to any given picture.

## Installing

This package was developed & tested under Python 3.9. Available on [PyPI](https://pypi.org/project/qqddm):

```bash
pip install --user qqddm
```

## Usage

Check the [example](example.py) code.

Since 2022-12-06, it seems that the API requires requests being performed from China, thus using a chinese proxy is required (you can see some public free servers [here](http://free-proxy.cz/en/proxylist/country/CN/socks5/ping/all)).

## Changelog

Versions 0.y.z are expected to be unstable, and the API may change on Minor (y) releases.

- 0.0.2
  - Add new `x-sign` headers required by the API since 2022-12-06.
  - Add new custom exceptions based on errors returned by the API: `VolumnLimitQQDDMApiResponseException`, `AuthFailedQQDDMApiResponseException`, `NotAllowedCountryQQDDMApiResponseException`, `NoFaceInPictureQQDDMApiResponseException`.
- 0.0.1
  - Initial release:
    - Class-based interface.
    - Pass an image (as bytes) and send it to QQ API, returning the resulting images URLs.
    - Download the returned images URLs.
    - Requests settings (different for QQ API and for downloading result images): request timeouts, proxy, user-agents.
