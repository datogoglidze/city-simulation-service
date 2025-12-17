import uvicorn
from typer import Typer

from app.runner.fastapi import FastApiConfig

cli = Typer(no_args_is_help=True, add_completion=False)


@cli.command()
def run(host: str = "0.0.0.0", port: int = 8000, root_path: str = "") -> None:
    uvicorn.run(
        app=FastApiConfig().setup(),
        host=host,
        port=port,
        root_path=root_path,
    )
