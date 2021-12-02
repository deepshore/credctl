import click

from .credentials import (
    CredentialsSecret,
    NamespaceDoesNotExistError,
    CannotConfigureClientError
)


@click.command()
@click.argument(
    'name',
    type=click.STRING
)
@click.argument(
    'username',
    type=click.STRING
)
@click.argument(
    'password',
    type=click.STRING
)
@click.option(
    'namespace',
    '-n', '--namespace',
    type=click.STRING,
    default='default'
)
def create(name, username, password, namespace):
    try:
        cs = CredentialsSecret(namespace=namespace)
        click.echo(cs.create(
            name=name,
            username=username,
            password=password
        ))
    except (NamespaceDoesNotExistError, CannotConfigureClientError) as e:
        click.echo(str(e))


@click.command()
@click.option(
    'namespace',
    '-n', '--namespace',
    type=click.STRING,
    default='default'
)
def list(namespace):
    try:
        cs = CredentialsSecret(namespace=namespace)
        click.echo(cs.list())
    except (NamespaceDoesNotExistError, CannotConfigureClientError) as e:
        click.echo(str(e))


@click.command()
@click.argument(
    'name',
    type=click.STRING
)
@click.option(
    'namespace',
    '-n', '--namespace',
    type=click.STRING,
    default='default'
)
def delete(name, namespace):
    try:
        cs = CredentialsSecret(namespace=namespace)
        click.echo(cs.delete(
            name=name
        ))
    except (NamespaceDoesNotExistError, CannotConfigureClientError) as e:
        click.echo(str(e))
