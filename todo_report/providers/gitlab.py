from todo_report.base import ITodoProvider


class GitLabProvider(ITodoProvider):
    api_base_url = "https://gitlab.com/api/v4/"

    @property
    def token_id(self):
        user = self.api.get("/user")
        return str(user["id"])
