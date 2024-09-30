# coding:utf-8

from base64 import b64encode
from datetime import datetime
import os
from typing import Optional
from urllib.parse import urljoin
from urllib.parse import urlparse
from urllib.parse import urlunparse

import requests


class page:
    def __init__(self, url: str):
        self.__url: str = url

    @property
    def url(self) -> str:
        return self.__url

    @property
    def label(self) -> str:
        encode: bytes = self.url.encode(encoding="utf-8")
        decode: str = b64encode(encode).decode(encoding="utf-8")
        return f"{datetime.now().strftime(f'%Y%m%d%H%M%S')}-{decode}"

    def save(self, path: Optional[str] = None) -> str:
        file: str = self.label if path is None else os.path.join(path, self.label) if os.path.isdir(path) else path  # noqa:E501
        with open(file=file, mode="w") as hdl:
            hdl.write(self.fetch())
        return file

    def fetch(self) -> str:
        response = requests.get(self.url)
        response.raise_for_status()
        return response.text


class site:
    def __init__(self, base: str):
        # self.__base: str = base
        components = urlparse(url=base)
        self.__scheme: str = components.scheme or "https"
        self.__netloc: str = components.netloc or components.path
        self.__scheme_and_netloc: str = urlunparse((self.scheme, self.netloc, '', '', '', ''))  # noqa:E501

    @property
    def scheme(self) -> str:
        return self.__scheme

    @property
    def netloc(self) -> str:
        return self.__netloc

    @property
    def scheme_and_netloc(self) -> str:
        return self.__scheme_and_netloc

    def page(self, *path: str) -> page:
        return page(urljoin(base=self.scheme_and_netloc, url="/".join(path)))
