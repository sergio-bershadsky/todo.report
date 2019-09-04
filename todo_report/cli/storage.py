import os
import re

from tinydb import TinyDB, where

CONFIG_ROOT = os.path.expanduser(os.path.join("~", ".todo.report"))


if not os.path.exists(CONFIG_ROOT):
    os.makedirs(CONFIG_ROOT, exist_ok=True)


db = TinyDB(os.path.join(CONFIG_ROOT, "storage.db"), indent=2)


def cam2dot(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1.\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1.\2', s1).lower()


class Model:

    @property
    def type(self):
        return cam2dot(self.__class__.__name__)

    @property
    def db(self):
        return db.table(self.type)


class AuthToken(Model):

    def create(self, token):
        return self.db.upsert(
            token, where("pk") == token["pk"]
        )
