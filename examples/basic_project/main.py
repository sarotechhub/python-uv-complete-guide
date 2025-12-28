import click
import requests


@click.command()
@click.option('--name', default='World', help='Name to greet.')
@click.option('--count', default=1, help='Number of greetings.')
def hello(name, count):
    """Simple greeting program."""
    for _ in range(count):
        click.echo(f'Hello {name}!')


def fetch_github_user(username):
    """Fetch GitHub user information."""
    response = requests.get(f'https://api.github.com/users/{username}')
    response.raise_for_status()
    return response.json()


if __name__ == '__main__':
    hello()
