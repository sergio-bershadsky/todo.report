from todo_report.base import ITodoProvider


class AsanaProvider(ITodoProvider):
    client_id = '1138234072422151'
    api_base_url = 'https://app.asana.com/api/1.0/'
    access_token_url = 'https://app.asana.com/-/oauth_token'
    authorize_url = 'https://app.asana.com/-/oauth_authorize'
    redirect_url = 'http://localhost:8000/authorize/asana'
    client_kwargs = {
        'scope': 'default',
    }
