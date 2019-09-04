import click
import requests


class TodoProviderType(type):

    registry = {}

    def __init__(cls, name, base, attrs):
        super().__init__(name, base, attrs)
        if not attrs.get("abstract"):
            name = cls.get_name()
            if name in TodoProviderType.registry:
                raise TypeError(f"Provider with name {name} already registered")
            TodoProviderType.registry[name] = cls


class Api:

    provider = None

    def __init__(self, provider):
        self.provider = provider


class RestApi(Api):

    def get(self, url, **params):
        return requests.get(
            f"{self.provider.api_base_url.rstrip('/')}{url}",
            params=params,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"{self.provider.token['token_type'].title()} {self.provider.token['access_token']}"
            }
        ).json()


class ITodoProvider(metaclass=TodoProviderType):

    abstract = True

    api_base_url: str
    token: str = None

    @property
    def api(self, cls=RestApi):
        return cls(provider=self)

    @classmethod
    def get_name(cls):
        return cls.__name__.lower().replace("provider", "")

    @property
    def name(self):
        return self.get_name()

    @property
    def token_id(self):
        raise NotImplementedError()

    def get_normalized_token(self):
        return {
            "pk": f"{self.token_id}@{self.name}",
            "token": self.token
        }


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
    def get(name: object) -> object:
        name = name.lower()
        if name not in TodoProviderType.registry:
            raise Exception(f"{name.capitalize()} provider not found")
        return TodoProviderType.registry[name]()


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
