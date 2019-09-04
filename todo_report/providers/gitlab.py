from todo_report.base import ITodoProvider


class GitLabProvider(ITodoProvider):
    client_id = '4fa36572f4baab04663d692d4507203cbe92e00bbfd0425ecff2347218f58f3d'
    api_base_url = 'https://gitlab.com/api/v4/'
    access_token_url = 'https://gitlab.com/oauth/token'
    authorize_url = 'https://gitlab.com/oauth/authorize'
    redirect_url = 'http://localhost:8000/authorize/gitlab'
    client_kwargs = {
        'scope': 'default',
    }
