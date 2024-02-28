__all__ = [
    "SrcPool",
    "copy_source",
    "move_source",
    "pull_source",
    "symlink_zig_projects",
    "symlink_rust_projects",
]


import os
import shutil
import subprocess as sp

from srcpool.utils import git_list_remote, git_split_url, repo_to_path


class SrcPool(object):
    def __init__(self, pool_path=None):
        self.pool_path = os.path.abspath(pool_path) if pool_path else None
        self.repo_set = set()

    def sync(self, src_path, sync_func):
        path = os.path.abspath(src_path)
        for root, directories, files in os.walk(path, followlinks=True):
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

    def git_clone(self, repo_file):
        for line in open(repo_file, "r"):
            repo_url = line.strip()
            if repo_url:
                try:
                    repo_info = git_split_url(line.strip())
                except ValueError as e:
                    raise e
                if repo_info not in self.repo_set:
                    clone_url(self.pool_path, repo_info, repo_url)
                    self.repo_set.add(repo_info)


def clone_url(pool_path, repo_info, repo_url):
    if pool_path is None:
        raise ValueError("pool_path is None")
    pool_repo_path = os.path.join(pool_path, repo_to_path(*repo_info))
    p = os.path.dirname(pool_repo_path)
    os.makedirs(p, exist_ok=True)
    if not os.path.exists(pool_repo_path):
        print("clone: %s in %s" % (str(repo_info), p))
        print("========")
        args = ["git", "clone", repo_url]
        sp.Popen(args, cwd=p).wait()
        print("========\n")


def copy_source(repo_info, repo_url, repo_path, pool_path):
    if pool_path is None:
        raise ValueError("pool_path is None")
    pool_repo_path = os.path.join(pool_path, repo_to_path(*repo_info))
    p = os.path.dirname(pool_repo_path)
    os.makedirs(p, exist_ok=True)
    if not os.path.exists(pool_repo_path):
        print("copytree: %s  %s" % (repo_path, pool_repo_path))
        shutil.copytree(repo_path, pool_repo_path, symlinks=True)


def move_source(repo_info, repo_url, repo_path, pool_path):
    if pool_path is None:
        raise ValueError("pool_path is None")
    pool_repo_path = os.path.join(pool_path, repo_to_path(*repo_info))
    p = os.path.dirname(pool_repo_path)
    os.makedirs(p, exist_ok=True)
    if not os.path.exists(pool_repo_path):
        print("move: %s  %s" % (repo_path, pool_repo_path))
        shutil.move(repo_path, pool_repo_path)


def pull_source(repo_info, repo_url, repo_path, pool_path):
    print("In %s\n=======" % repo_path)
    args = ["git", "pull"]
    sp.Popen(args, cwd=repo_path).wait()
    print("========\n")


def symlink_zig_projects(repo_info, repo_url, repo_path, pool_path):
    if os.path.exists(os.path.join(repo_path, "build.zig")):
        print("In %s\n=======" % repo_path)
        name = os.path.basename(repo_path)
        link_path = os.path.join(pool_path, name)
        if os.path.exists(link_path):
            print("Skip - link already exists")
        else:
            os.symlink(repo_path, link_path)
        print("========\n")


def symlink_rust_projects(repo_info, repo_url, repo_path, pool_path):
    if os.path.exists(os.path.join(repo_path, "Cargo.toml")):
        print("In %s\n=======" % repo_path)
        name = os.path.basename(repo_path)
        link_path = os.path.join(pool_path, name)
        if os.path.exists(link_path):
            print("Skip - link already exists")
        else:
            os.symlink(repo_path, link_path)

        print("========\n")
