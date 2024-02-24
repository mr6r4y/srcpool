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
)


@click.group()
@click.pass_context
def srcpool(
    ctx,
):
    ctx.ensure_object(dict)


@srcpool.command()
@click.pass_context
@click.argument("source-path")
def list_source(ctx, source_path):
    ctx.obj["source_path"] = os.path.abspath(source_path)
    s = SrcPool()
    s.sync(
        ctx.obj["source_path"],
        lambda repo_info, repo_url, repo_path, pool_path: print(
            [repo_info, repo_url, repo_path]
        ),
    )


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
