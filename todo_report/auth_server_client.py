import requests


class AuthServerClient:

    @property
    def server_url(self):
        #return "http://localhost:8000/"
        return "https://urbamatica.appspot.com/"

    def get_authorize_url(self, provider):
        return self.call("get_authorize_url", "get", provider=provider)

    def get_token(self, state):
        return self.call("get_token", "post", state=state)

    def call(self, name, method, **params):
        server_url = self.server_url.rstrip("/")
        response = requests.request(
            method,
            f"{server_url}/{name}",
            params=params if method.lower() == "get" else None,
            data=params if method.lower() != "get" else None
        )
        try:
            result = response.json()
        except ValueError:
            result = response.content

        return result
