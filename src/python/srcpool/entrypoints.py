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
    archive,
)
from srcpool.gitea import Gitea


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
def clone(ctx, pool_path, repo_file):
    ctx.obj["pool_path"] = os.path.abspath(pool_path)
    ctx.obj["repo_file"] = os.path.abspath(repo_file)
    s = SrcPool(ctx.obj["pool_path"])
    s.git_clone(ctx.obj["repo_file"])


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
@click.argument("url")
def gitea(ctx, url):
    g = Gitea(url)
    for r in g.repositories():
        print(r)
