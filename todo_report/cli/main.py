import time
import click
import click_spinner

from todo_report.auth_server_client import AuthServerClient
from todo_report.base import ITodoProvider, Provider
from todo_report.cli.storage import AuthToken


MAX_TRIES = 30


@click.group("cli")
def cli():
    pass


@cli.command()
@click.argument(
    'provider',
    type=Provider()
)
def add(provider: ITodoProvider):
    tries = 0
    token = 0
    url, state = AuthServerClient().get_authorize_url(provider.name)

    with click_spinner.spinner():
        click.launch(url)

    with click_spinner.spinner(beep=True):
        while True:
            if tries > MAX_TRIES:
                break

            token = AuthServerClient().get_token(state)
            if isinstance(token, dict):
                break
            time.sleep(1)
            tries += 1

    provider.token = token

    AuthToken().create(provider.get_normalized_token())


if __name__ == '__main__':
    cli()
