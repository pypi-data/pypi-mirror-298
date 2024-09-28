from typing import Annotated, Optional

import typer

from .utils import _filter_external_dependencies, _install_apt, _install_s3, _list_external_dependencies

app = typer.Typer(rich_markup_mode='rich')

DEFAULT_BUCKET = 'skcr-public-static-build'
DEFAUT_INSTALL_DIR = '/usr/local/bin/'


@app.command(name='apt')
def install_using_apt(
    prefix: Annotated[Optional[str], typer.Option(help='Filter out some external dependencies')] = 'pkg:generic/',
) -> None:
    """Install the required external dependencies using apt."""
    deps = _list_external_dependencies()
    filtered = _filter_external_dependencies(deps, prefix)
    _install_apt(filtered)


@app.command(name='s3')
def install_using_s3(
    prefix: Annotated[Optional[str], typer.Option(help='Filter out some external dependencies')] = 'pkg:generic/',
    bucket: Annotated[str, typer.Option(help='The s3 bucket to download the dependencies from')] = DEFAULT_BUCKET,
    install_dir: Annotated[str, typer.Option(help='The directory to install the dependencies to')] = DEFAUT_INSTALL_DIR,
) -> None:
    """Install the required external dependencies using static builds from an s3 bucket."""
    deps = _list_external_dependencies()
    filtered = _filter_external_dependencies(deps, prefix)
    _install_s3(filtered, bucket, install_dir)


if __name__ == '__main__':
    app()
