__all__ = [
    "Gitea",
]


from urllib.parse import urljoin
import sys
import requests


class Gitea(object):
    def __init__(self, url):
        self.url = url
        self.session = requests.session()

    def repositories(self, page=1):
        while True:
            u = urljoin(self.url, "api/v1/repos/search?page=%i" % page)
            r = self.session.get(u)
            if not r.json().get("ok", True):
                page += 1
                continue
            dt = r.json().get("data", [])
            print("Page=%i" % page, file=sys.stderr)
            for item in dt:
                yield item.get("clone_url")
            page += 1
            if len(dt) == 0:
                break
