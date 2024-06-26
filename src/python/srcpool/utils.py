__all__ = [
    "git_list_remote",
    "git_split_url",
    "repo_to_path",
]

import os
import subprocess


def git_list_remote(repo_path):
    cmd = ["git", "config", "remote.origin.url"]

    (stdout, stderr) = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, cwd=repo_path
    ).communicate()
    r = stdout.strip().decode("ascii")
    return r if r else None


def git_split_url(url):
    if url.startswith("git@") or url.startswith("gitlab@"):
        domain, path = url[4:].strip("/").split(":", maxsplit=1)
    elif url.startswith("https://"):
        domain, path = url[8:].strip("/").split("/", maxsplit=1)
    elif url.startswith("git://"):
        domain, path = url[6:].strip("/").split("/", maxsplit=1)
    elif url.startswith("http://"):
        domain, path = url[7:].strip("/").split("/", maxsplit=1)
    else:
        raise ValueError("Unknown type of URL: %s" % url)

    owner = os.path.dirname(path)
    repo_name, ext = os.path.splitext(os.path.basename(path))
    if ext != ".git":
        repo_name += ext

    return (domain, owner if owner else None, repo_name)


def repo_to_path(domain, owner, name):
    paths = [domain]
    if owner:
        paths.append(owner)
    paths.append(name)
    return os.path.join(*paths)
