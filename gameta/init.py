import json
from os.path import splitext, basename, normpath, abspath
from typing import Dict, Optional

import click

from git import Repo, InvalidGitRepositoryError

from . import gameta_cli, gameta_context, GametaContext


__all__ = ['init', 'sync']


@gameta_cli.command()
@click.option('--git', '-g', is_flag=True, default=False, help='Flag to initialise the current directory as a git repo')
@click.option('--overwrite', '-o', is_flag=True, default=False, help='Flag to overwrite existing .meta file')
@gameta_context
def init(context: GametaContext, overwrite: bool, git: bool) -> None:
    """
    Initialises a repository as a metarepo
    \f
    Args:
        context (GametaContext): Gameta Context
        overwrite (bool): Flag to indicate if existing .meta file should be overwritten
        git (bool): Flag to indicate if we should initialise git in the current directory

    Returns:
        None

    Examples:
        $ gameta init  # With default values
        $ gameta init -g  # Initialises the current working directory as a git repository
        $ gameta init -o  # Overwrites the existing .meta file if it exists
    """
    click.echo(f"Initialising metarepo in {context.project_dir}")

    try:
        repo: Repo = Repo(context.project_dir)
        name: str = splitext(basename(repo.remote().url))[0]
        url: Optional[str] = repo.remote().url
    except InvalidGitRepositoryError:
        if git is False:
            raise click.ClickException(f"{context.project_dir} is not a valid git repo, initialise it with -g flag")
        click.echo(f"Initialising {context.project_dir} as a git repository")
        Repo.init(context.project_dir)
        name: str = basename(context.project_dir)
        url: Optional[str] = None

    if context.is_metarepo and overwrite is False:
        click.echo(f"{context.project_dir} is a metarepo, ignoring")
        return

    context.repositories[name] = {
        'url': url,
        'path': '.',
        'tags': ['metarepo']
    }
    context.export()
    click.secho(f"Successfully initialised {name} as a metarepo")


@gameta_cli.command()
@gameta_context
def sync(context: GametaContext) -> None:
    """
    Syncs all the repositories listed in the .meta file locally
    \f
    Args:
        context (GametaContext): Gameta Context

    Returns:
        None

    Examples:
        $ gameta sync
    """
    click.echo(f"Syncing all child repositories in metarepo {context.project_dir}")
    for repo, details in context.repositories.items():

        # We assume the metarepo has already been cloned
        if abspath(details["path"]) == context.project_dir:
            continue

        Repo.clone_from(details['url'], details['path'])
        click.echo(f'Successfully synced {repo} to {details["path"]}')