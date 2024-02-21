__all__ = [
    "srcpool",
]

import os
import click
from srcpool import SrcPool, copy_source, move_source


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
