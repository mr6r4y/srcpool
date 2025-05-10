__all__ = [
    "Launchpad",
]


from urllib.parse import urljoin
import requests
from ptpython.repl import embed


class Launchpad(object):
    def __init__(self):
        self.url = "https://api.launchpad.net/1.0/"
        self.session = requests.session()

    def repositories(self):
        git_repo_u = "https://git.launchpad.net/ubuntu/+source/%s"
        git_repo_owner_u = "https://git.launchpad.net/~%s/ubuntu/+source/%s"
        u = urljoin(self.url, "projects")
        while True:
            r = self.session.get(u)
            # embed(
            #     globals(),
            #     locals(),
            # )
            # break

            j = r.json()
            dt = j.get("entries", [])
            for item in dt:
                if (
                    not item.get("private")
                    and item.get("active")
                    and item.get("vcs") == "Git"
                    and item.get("official_codehosting")
                ):
                    owner = item.get("owner_link")
                    if owner:
                        owner = owner.split("~")[1]
                        yield git_repo_owner_u % (owner, item.get("name"))
                    else:
                        yield git_repo_u % item.get("name")
            u = j.get("next_collection_link")
            if not u:
                break

    def projects(self):
        u = urljoin(self.url, "projects")
        while True:
            r = self.session.get(u)

            j = r.json()
            dt = j.get("entries", [])
            for item in dt:
                yield item.get("web_link")
            u = j.get("next_collection_link")
            if not u:
                break
