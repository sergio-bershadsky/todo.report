from todo_report.base import ITodoProvider


class AsanaProvider(ITodoProvider):
    api_base_url = "https://app.asana.com/api/1.0/"

    @property
    def token_id(self):
        return str(self.token["data"]["id"])
