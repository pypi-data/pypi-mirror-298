import click
from rudydesplan_de_toolkit.vm import start, stop, connect

@click.group()
def cli():
    print("CLI is running...")

cli.add_command(start)
cli.add_command(stop)
cli.add_command(connect)

if __name__ == '__main__':
    cli()
