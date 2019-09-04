import json
import time

import click
import click_spinner

from todo_report.auth_server_client import AuthServerClient
from todo_report.base import ProviderManager, ITodoProvider


class Provider(click.Choice):

    def __init__(self):
        self.case_sensitive = True
        super(Provider, self).__init__(
            ProviderManager.list(),
            case_sensitive=True
        )

    def convert(self, value, param, ctx):
        result = super().convert(value, param, ctx)
        return ProviderManager()[result]


@click.group("cli")
def cli():
    pass


@cli.command()
@click.argument(
    'provider',
    type=Provider()
)
def add(provider: ITodoProvider):
    url, state = AuthServerClient().get_authorize_url(provider.name)

    with click_spinner.spinner():
        click.launch(url)

    with click_spinner.spinner(beep=True):
        while True:
            token = AuthServerClient().get_token(state)
            if isinstance(token, dict):
                break
    print(token)


if __name__ == '__main__':
    cli()
