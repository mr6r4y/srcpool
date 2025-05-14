__all__ = [
    "Github",
]


from urllib.parse import urljoin
import requests


class Github(object):
    def __init__(self):
        self.url = "https://api.github.com/%s/%s/repos?per_page=1000&page=%i"
        self.url_user = "https://api.github.com/users/%s"
        self.session = requests.session()

    def repositories(self, account, forks=False):
        u = self.session.get(self.url_user % account)
        uj = u.json()
        tp = "users" if uj.get("type") == "User" else "orgs"
        page = 1
        while True:
            r = self.session.get(self.url % (tp, account, page))
            rj = r.json()
            if len(rj) == 0:
                break
            for i in rj:
                if i["fork"] and forks:
                    yield i["clone_url"]
                elif not i["fork"] and not forks:
                    yield i["clone_url"]
            page += 1
