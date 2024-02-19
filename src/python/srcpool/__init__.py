__all__ = [
    "SrcPool",
]


import os

from srcpool.utils import git_list_remote, git_split_url


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
