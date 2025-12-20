__all__ = [
    "Gitlab",
]


from urllib.parse import urljoin
import sys
import requests


class Gitlab(object):
    def __init__(self, url):
        self.url = url
        self.session = requests.session()

    def repositories(self, username=None, page=1):
        while True:
            if username:
                u = urljoin(
                    self.url, "api/v4/users/%s/projects?page=%i" % (username, page)
                )
            else:
                u = urljoin(self.url, "api/v4/projects?page=%i" % page)
            r = self.session.get(u)
            if r.status_code != 200:
                print("Get ERROR: %s" % r.text, file=sys.stderr)
                break

            if username:
                dt = r.json()
            else:
                dt = r.json()
            print("Page=%i" % page, file=sys.stderr)
            for item in dt:
                yield item.get("http_url_to_repo")
            page += 1
            if len(dt) == 0:
                break
