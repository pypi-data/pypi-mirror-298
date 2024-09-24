import click

from .init_agentic import init_agentic
from .run_agentic import run_agentic


@click.group()
def agenticos():
    """Top-level command group for agenticos."""


@click.command()
@click.option("-b", "--backend", type=click.Choice(["crewai"]), default="crewai")
@click.option("-f", "--force", is_flag=True, help="Overwrite existing files")
def init(backend, force):
    """Initialize a new AgenticOS project. Has to be run in the root folder of your project."""
    click.echo(
        "Initializing a new AgenticOS project... with backend: {}".format(backend)
    )
    init_agentic(backend, force)


@click.command()
@click.option("-M", "--mode", type=click.Choice(["httpserver"]), default="httpserver")
@click.option("-P", "--port", type=int, default=8000)
@click.option("--dev", is_flag=True, help="Run in development mode")
def run(mode, port, dev):
    """Run agentic node."""
    click.echo("Running agenic in {} mode".format(mode))
    run_agentic(mode, port, dev)


agenticos.add_command(init)
agenticos.add_command(run)
