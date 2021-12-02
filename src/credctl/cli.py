import click

from .commands import create, delete, list


@click.group()
def main():
    pass


main.add_command(create)
main.add_command(delete)
main.add_command(list)
