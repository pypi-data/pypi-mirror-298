import click

from whipweb.settings import LOGGING_CONFIG


@click.group()
def cli():
    pass


@cli.command()
@click.option("--host", default="0.0.0.0")
@click.option("--port", default=8080)
@click.option("--reload", is_flag=True)
def run(host, port, reload):
    import uvicorn

    uvicorn.run(
        "whipweb.app:app",
        host=host,
        port=port,
        reload=reload,
        log_config=LOGGING_CONFIG,
    )
