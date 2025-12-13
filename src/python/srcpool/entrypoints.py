__all__ = [
    "srcpool",
]

import os
import click
from srcpool import (
    SrcPool,
    copy_source,
    move_source,
    pull_source,
    symlink_zig_projects,
    symlink_rust_projects,
    symlink_c3_projects,
    archive,
)
from srcpool.gitea import Gitea
from srcpool.github import Github
from srcpool.launchpad import Launchpad


@click.group()
@click.pass_context
def srcpool(
    ctx,
):
    ctx.ensure_object(dict)


@srcpool.command()
@click.pass_context
@click.argument("source-path")
@click.option("--only-url", is_flag=True, default=False)
def list_source(ctx, source_path, only_url):
    ctx.obj["source_path"] = os.path.abspath(source_path)
    s = SrcPool()
    if only_url:
        fn = lambda repo_info, repo_url, repo_path, pool_path: print(repo_url)
    else:
        fn = lambda repo_info, repo_url, repo_path, pool_path: print(
            [repo_info, repo_url, repo_path]
        )

    s.sync(ctx.obj["source_path"], fn)


@srcpool.command()
@click.pass_context
@click.argument("source-path")
def git_pull(ctx, source_path):
    ctx.obj["source_path"] = os.path.abspath(source_path)
    s = SrcPool()
    s.sync(
        ctx.obj["source_path"],
        pull_source,
    )


@srcpool.command()
@click.pass_context
@click.argument("source-path")
@click.argument("tag-path")
def symlink_zig(ctx, source_path, tag_path):
    ctx.obj["source_path"] = os.path.abspath(source_path)
    ctx.obj["tag_path"] = os.path.abspath(tag_path)
    s = SrcPool(ctx.obj["tag_path"])
    s.sync(
        ctx.obj["source_path"],
        symlink_zig_projects,
    )


@srcpool.command()
@click.pass_context
@click.argument("source-path")
@click.argument("tag-path")
def symlink_rust(ctx, source_path, tag_path):
    ctx.obj["source_path"] = os.path.abspath(source_path)
    ctx.obj["tag_path"] = os.path.abspath(tag_path)
    s = SrcPool(ctx.obj["tag_path"])
    s.sync(
        ctx.obj["source_path"],
        symlink_rust_projects,
    )


@srcpool.command()
@click.pass_context
@click.argument("source-path")
@click.argument("tag-path")
def symlink_c3(ctx, source_path, tag_path):
    ctx.obj["source_path"] = os.path.abspath(source_path)
    ctx.obj["tag_path"] = os.path.abspath(tag_path)
    s = SrcPool(ctx.obj["tag_path"])
    s.sync(
        ctx.obj["source_path"],
        symlink_c3_projects,
    )


@srcpool.command()
@click.pass_context
@click.argument("pool-path")
@click.argument("source-path")
def copy(ctx, pool_path, source_path):
    ctx.obj["pool_path"] = os.path.abspath(pool_path)
    ctx.obj["source_path"] = os.path.abspath(source_path)
    s = SrcPool(ctx.obj["pool_path"])
    s.sync(
        ctx.obj["source_path"],
        copy_source,
    )


@srcpool.command()
@click.pass_context
@click.argument("pool-path")
@click.argument("source-path")
def move(ctx, pool_path, source_path):
    ctx.obj["pool_path"] = os.path.abspath(pool_path)
    ctx.obj["source_path"] = os.path.abspath(source_path)
    s = SrcPool(ctx.obj["pool_path"])
    s.sync(
        ctx.obj["source_path"],
        move_source,
    )


@srcpool.command()
@click.pass_context
@click.argument("pool-path")
@click.argument("repo-file")
@click.option(
    "-s",
    "--skip-first",
    type=click.INT,
    help="Skip the first N lines of the repository file",
)
def clone(ctx, pool_path, repo_file, skip_first):
    ctx.obj["pool_path"] = os.path.abspath(pool_path)
    ctx.obj["repo_file"] = os.path.abspath(repo_file)
    s = SrcPool(ctx.obj["pool_path"])
    s.git_clone(ctx.obj["repo_file"], skip_first=skip_first)


@srcpool.command()
@click.pass_context
@click.argument("pool-path")
@click.argument("backup-dir")
def backup(ctx, pool_path, backup_dir):
    ctx.obj["pool_path"] = os.path.abspath(pool_path)
    ctx.obj["backup_dir"] = os.path.abspath(backup_dir)
    s = SrcPool(ctx.obj["pool_path"])
    s.sync(
        ctx.obj["pool_path"],
        archive(ctx.obj["backup_dir"]),
    )


@srcpool.command()
@click.pass_context
@click.argument("account")
@click.option("-f", "--forks", is_flag=True, default=False)
def github(ctx, account, forks):
    g = Github()
    for r in g.repositories(account, forks):
        print(r)


@srcpool.command()
@click.pass_context
@click.argument("url")
@click.option("-u", "--username", default=None)
@click.option("-p", "--page", type=click.INT, default=1)
def gitea(ctx, url, username, page):
    g = Gitea(url)
    for r in g.repositories(username=username, page=page):
        print(r)


@srcpool.command()
@click.pass_context
def launchpad(ctx):
    g = Launchpad()
    for r in g.repositories():
        print(r)
