from todo_report.base import ITodoProvider


class BitBucketProvider(ITodoProvider):
    api_base_url = "https://api.bitbucket.org/2.0/"

    @property
    def token_id(self):
        user = self.api.get("/user")
        return str(user["account_id"])
