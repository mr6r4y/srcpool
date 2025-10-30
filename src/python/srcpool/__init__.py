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

    def git_clone(self, repo_file, skip_first=None):
        for n, line in enumerate(open(repo_file, "r"), start=1):
            if line.strip().startswith("#"):
                continue
            if skip_first and skip_first > 0 and skip_first >= n:
                print(
                    "Skip: n: %i, skip-first: %i, line: %s"
                    % (n, skip_first, line.strip())
                )
                continue
            repo_url = line.strip()
            if repo_url:
                try:
                    repo_info = git_split_url(line.strip())
                except ValueError as e:
                    raise e
                if repo_info not in self.repo_set:
                    clone_url(self.pool_path, repo_info, repo_url)
                    self.repo_set.add(repo_info)


def archive(backup_dir):
    def _(repo_info, repo_url, repo_path, pool_path):
        tar_gz_file = (
            "_".join(
                [(i.replace("/", "_") if i is not None else "") for i in repo_info]
            )
            + ".tar.gz"
        )
        tar_gz_path = os.path.join(backup_dir, tar_gz_file)
        params = [
            "tar",
            "-czf",
            tar_gz_path,
            "-C",
            pool_path,
            repo_path[len(pool_path) + 1 :],
        ]
        # TO-DO: Make param to control update/skip behaviour
        if os.path.exists(tar_gz_path):
            t1 = os.path.getmtime(repo_path)
            t2 = os.path.getctime(tar_gz_path)
            if t1 > t2:
                print("Update %s" % tar_gz_path)
                print(" ".join(params))
                sp.Popen(params).wait()
            else:
                print("Skip %s" % tar_gz_path)

        else:
            print(" ".join(params))
            sp.Popen(params).wait()

    return _


def path_in_git_repo(path):
    path = os.path.dirname(path)
    while len(path) > 1:
        if os.path.exists(path):
            if ".git" in os.listdir(path):
                return True
        path = os.path.dirname(path)
    return False


def clone_url(pool_path, repo_info, repo_url):
    if pool_path is None:
        raise ValueError("pool_path is None")
    pool_repo_path = os.path.join(pool_path, repo_to_path(*repo_info))
    p = os.path.dirname(pool_repo_path)
    os.makedirs(p, exist_ok=True)
    if path_in_git_repo(pool_repo_path):
        print("Invalid: Path in another git repo: %s" % pool_repo_path)
        return
    if not os.path.exists(pool_repo_path):
        print("clone: %s in %s" % (str(repo_info), p))
        print("========")
        args = ["git", "clone", repo_url]
        sp.Popen(args, cwd=p).wait()
        print("========\n")
    else:
        print("Skip: Path exists: %s" % pool_repo_path)


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


def symlink_c3_projects(repo_info, repo_url, repo_path, pool_path):
    if os.path.exists(os.path.join(repo_path, "project.json")):
        print("In %s\n=======" % repo_path)
        name = os.path.basename(repo_path)
        link_path = os.path.join(pool_path, name)
        if os.path.exists(link_path):
            print("Skip - link already exists")
        else:
            os.symlink(repo_path, link_path)

        print("========\n")
