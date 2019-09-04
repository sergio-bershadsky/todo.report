from authlib.client import OAuth2Session

from todo_report.auth_server_client import AuthServerClient


class TodoProviderType(type):

    registry = {}

    def __init__(cls, name, base, attrs):
        super().__init__(name, base, attrs)
        if not attrs.get("abstract"):
            TodoProviderType.registry[cls.get_name()] = cls


class ITodoProvider(metaclass=TodoProviderType):

    abstract = True
    client_id: str
    api_base_url: str
    access_token_url: str
    authorize_url: str
    client_kwargs: dict

    @classmethod
    def get_name(cls):
        return cls.__name__.lower().replace("provider", "")

    @property
    def name(self):
        return self.get_name()

    @property
    def redirect_url(self) -> str:
        server_url = AuthServerClient().server_url.rstrip("/")
        return f"{server_url}/authorize/{self.get_name()}"

    @property
    def conf(self):
        return {k: v for k, v in self.__dict__.items() if k != "abstract"}

    def get_authorize_url(self):
        session = OAuth2Session(
            client_id=self.client_id,
        )
        with session as s:
            s.redirect_uri = self.redirect_url
            url, state = s.create_authorization_url(
                self.authorize_url
            )
            return url


class ProviderManager:

    def __getattr__(self, name: str) -> ITodoProvider:
        return self.get(name)

    def __getitem__(self, name: str) -> ITodoProvider:
        return self.get(name)

    def __contains__(self, name: str) -> bool:
        return name in TodoProviderType.registry

    @staticmethod
    def list() -> list:
        return list(TodoProviderType.registry.keys())

    @staticmethod
    def get(name) -> ITodoProvider:
        name = name.lower()
        if name not in TodoProviderType.registry:
            raise Exception(f"{name.capitalize()} provider not found")
        return TodoProviderType.registry[name]()
