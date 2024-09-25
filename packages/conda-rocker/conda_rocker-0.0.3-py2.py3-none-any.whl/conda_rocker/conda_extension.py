import pkgutil
from rocker.extensions import RockerExtension
import typing


class CondaExtension(RockerExtension):
    @staticmethod
    def get_name():
        return "conda"

    def __init__(self):
        self.name = CondaExtension.get_name()

    def get_snippet(self, cliargs):
        return pkgutil.get_data(
            "conda_rocker", "templates/{}_snippet.Dockerfile".format(self.name)
        ).decode("utf-8")

    def get_user_snippet(self, cliargs):
        return pkgutil.get_data(
            "conda_rocker", "templates/{}_user_snippet.Dockerfile".format(self.name)
        ).decode("utf-8")

    def invoke_after(self, cliargs) -> typing.Set[str]:
        return set(["user"])

    def required(self, cliargs) -> typing.Set[str]:
        return set(["user"])

    @staticmethod
    def register_arguments(parser, defaults=None):
        if defaults is None:
            defaults = {}
        parser.add_argument(
            f"--{CondaExtension.get_name()}",
            action="store_true",
            default=defaults.get("conda"),
            help="add conda to your docker image",
        )
