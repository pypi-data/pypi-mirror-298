import click
import subprocess

@click.group()
def cli():
    pass

@click.command()
def start():
    """Start your vm"""
    click.echo("Starting the VM...")
    subprocess.run(["gcloud", "compute", "instances", "start", "--zone=europe-west1-d", "lewagon-data-eng-vm-rudydesplan"], check=True)


@click.command()
def stop():
    """Stop your vm"""
    click.echo("Stopping the VM...")
    subprocess.run(["gcloud", "compute", "instances", "stop", "--zone=europe-west1-d", "lewagon-data-eng-vm-rudydesplan"], check=True)


@click.command()
def connect():
    """Connect to your vm in vscode inside your ~/code/rudydesplan/ folder"""
    click.echo("Connecting to the VM...")
    subprocess.run(["code", "--folder-uri", "vscode-remote://ssh-remote+desrudy@130.211.105.231/home/desrudy/code/rudydesplan/"], check=True)

cli.add_command(start)
cli.add_command(stop)
cli.add_command(connect)
