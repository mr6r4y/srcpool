__all__ = [
    "SrcPool",
    "copy_source",
    "move_source",
    "clone_source",
]


import os
import shutil

from srcpool.utils import git_list_remote, git_split_url, repo_to_path


class SrcPool(object):
    def __init__(self, pool_path):
        self.pool_path = os.path.abspath(pool_path)
        self.repo_set = set()

    def sync(self, src_path, sync_func):
        path = os.path.abspath(src_path)
        for root, directories, files in os.walk(path):
            if ".git" in directories:
                repo_url = git_list_remote(root)
                if repo_url:
                    try:
                        repo_info = git_split_url(repo_url)
                    except ValueError as e:
                        print(root)
                        raise e
                    if repo_info not in self.repo_set:
                        sync_func(repo_info, repo_url, root, self.pool_path)
                        self.repo_set.add(repo_info)
                        del directories[:]


def copy_source(repo_info, repo_url, repo_path, pool_path):
    pool_repo_path = os.path.join(pool_path, repo_to_path(*repo_info))
    p = os.path.dirname(pool_repo_path)
    os.makedirs(p, exits_ok=True)
    if not os.path.exists(pool_repo_path):
        print("copytree: %s  %s" % (repo_path, pool_repo_path))
        shutil.copytree(repo_path, pool_repo_path, symlinks=True)


def move_source(repo_info, repo_url, repo_path, pool_path):
    pool_repo_path = os.path.join(pool_path, repo_to_path(*repo_info))
    p = os.path.dirname(pool_repo_path)
    os.makedirs(p, exits_ok=True)
    if not os.path.exists(pool_repo_path):
        print("move: %s  %s" % (repo_path, pool_repo_path))
        shutil.move(repo_path, pool_repo_path)


def clone_source(repo_info, repo_url, repo_path, pool_path):
    pass
