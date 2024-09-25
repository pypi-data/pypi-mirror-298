import os
from typing import Callable, TypeAlias

from cleo.commands.command import Command
from cleo.helpers import argument, option

# from cleo.io.io import IO
from poetry.config.config import Config
from poetry.console.application import Application
from poetry.plugins.application_plugin import ApplicationPlugin
from poetry.poetry import Poetry
from poetry.repositories.legacy_repository import LegacyRepository
from poetry.repositories.repository_pool import RepositoryPool
from poetry.utils.password_manager import PasswordManager

ADO_HOSTNAME = "https://pkgs.dev.azure.com"
ADO_FEED_URL = "https://pkgs.dev.azure.com/{organization}/_packaging/{feed_name}/pypi/simple/"

Organization: TypeAlias = str
FeedName: TypeAlias = str


def set_access_token(
    feed_name: str, username: str, access_token: str, config: Config
) -> None:
    """Set access token with the poetry passwordmanager."""
    password_manager = PasswordManager(config=config)
    password_manager.set_http_password(
        repo_name=feed_name,
        username=username,
        password=access_token,
    )


def get_access_token(
    feed_name: str,
    config: Config,
) -> dict[str, str | None] | None:
    """Get the access token configured with poetry for the artifact feed."""
    password_manager = PasswordManager(config=config)
    access_token = password_manager.get_http_auth(repo_name=feed_name)
    return access_token


def add_artifact_feed(
    feed_name: str,
    index_url: str,
    poetry: Poetry,
    config: Config,
) -> None:
    """Add artifact feed as a repository for the current Poetry Session."""
    repository = LegacyRepository(
        name=feed_name,
        url=index_url,
        config=config,
    )
    poetry.pool.add_repository(
        repository=repository,
        secondary=False,
    )


def source_already_configured(
    index_url: str, repository_pool: RepositoryPool
) -> bool:
    """Check if a repository has already been configured with the index_url."""
    return any(
        repository.url in index_url  # type: ignore
        for repository in repository_pool.repositories
    )


def get_index_url(organization: str, feed_name: str) -> str:
    """Construct a valid artifact feed url from organization and feed name."""
    return ADO_FEED_URL.format(organization=organization, feed_name=feed_name)


def configure_azure_devops(
    poetry: Poetry,
) -> None:
    """Configure Poetry with azure devops artifact feeds."""
    config = Config.create()
    azure_devops_config = config.get("azure-devops")

    if not azure_devops_config:
        return

    for feed_name, feed_config in azure_devops_config.items():
        username = feed_config.get("username")
        organization = feed_config.get("organization")

        if credentials := get_access_token(feed_name=feed_name, config=config):
            token = credentials.get("password")
        else:
            token = feed_config.get("token") or os.environ.get(
                "AZURE_DEVOPS_EXT_PAT"
            )
        if organization and token and username:
            # Create the index url from organization and feed name
            index_url = get_index_url(
                organization=organization,
                feed_name=feed_name,
            )
            if not poetry.pool.has_repository(feed_name):
                if not source_already_configured(
                    index_url=index_url, repository_pool=poetry.pool
                ):
                    add_artifact_feed(
                        feed_name=feed_name,
                        index_url=index_url,
                        poetry=poetry,
                        config=config,
                    )
            if not get_access_token(feed_name=feed_name, config=config):
                set_access_token(
                    feed_name=feed_name,
                    username=username,
                    access_token=token,
                    config=config,
                )


def get_command_factory(command: type[Command]) -> Callable[[], Command]:
    """Get a factory for the command type.

    Wraps command type in a function, which initializes and returns said
    command when called. Used for deffered command initialization, as required
    by Poetry.
    """
    return lambda *args, **kwargs: command()  # type: ignore


def register_commands(
    application: Application, commands: list[type[Command]]
) -> None:
    """Register commands with Poetry."""
    for command in commands:
        if command.name:
            application.command_loader.register_factory(
                command.name, get_command_factory(command)
            )


def validate_index_url(index_url: str) -> tuple[Organization, FeedName]:
    """Validate that index_url is a valid artifact feed url."""
    if not index_url.startswith(ADO_HOSTNAME):
        raise ValueError(
            "Invalid <index_url>, must be a valid URL starting with "
            f'"{ADO_HOSTNAME}": {index_url}'
        )
    parts = index_url.replace("https://pkgs.dev.azure.com/", "").split("/")
    return parts[0], parts[2]


class AddCommand(Command):
    """
    Add artifact feed to Poetry.

    azure add
        {index-url? : URL to the artifact feed}
        {--username : Username to authenticate as}
        {--access-token : Token to authenticate with}
        {--feed-name : Name of the artifact feed}
        {--organization : Name of organization hosting the feed}
    """

    name = "azure add"
    description = "Add artifact feed to Poetry."
    arguments = [
        argument(
            "index-url",
            description="URL for the artifact feed",
            optional=True,
        ),
    ]
    options = [
        option(
            "organization",
            description="The organization hosting the artifact feed",
            value_required=True,
            flag=False,
        ),
        option(
            "feed-name",
            description="Name of the artifact feed.",
            value_required=True,
            flag=False,
        ),
        option(
            "username",
            description="Username to authenticate as.",
            value_required=True,
            flag=False,
        ),
        option(
            "access-token",
            description="Access token to authenticate with.",
            value_required=True,
            flag=False,
        ),
    ]

    def handle(self) -> int:
        """Execute Add command."""
        config = Config.create()
        index_url = self.argument("index-url")
        username = self.option("username") or os.environ.get(
            "AZURE_DEVOPS_EXT_USERNAME"
        )
        if not username:
            raise ValueError(
                "Please provide a username to authenticate as, either via "
                "'--username <my-username>' or the environment variable "
                "AZURE_DEVOPS_EXT_USERNAME."
            )
        if index_url:
            organization, feed_name = validate_index_url(index_url=index_url)
        else:
            organization = self.option("organization")
            feed_name = self.option("feed-name")
        if not organization and feed_name:
            raise ValueError(
                "Could not resolve artifact feed: please provide a URL "
                "`azure add <index-url>` or by "
                "`azure add --organization <name> --feed-name <name>`"
            )
        if access_token := (
            self.option("access-token")
            or os.environ.get("AZURE_DEVOPS_EXT_PAT")
        ):
            set_access_token(
                feed_name=feed_name,
                username=username,
                access_token=access_token,
                config=config,
            )
        else:
            raise ValueError(
                "Please provide an Access Token, either via --access-token or "
                "the environment variable AZURE_DEVOPS_EXT_USERNAME"
            )
        azure_devops_config = config.get("azure-devops", {})
        azure_devops_config.update(
            {
                feed_name: {
                    "organization": organization,
                    "username": username,
                }
            }
        )
        # Persist the settings by adding property to the config source.
        config.config_source.add_property("azure-devops", azure_devops_config)
        return 0


class AzurePoetryPlugin(ApplicationPlugin):
    """Plugin supporting azure artifact feeds as private repositories."""

    _commands: list[type[Command]] = [
        AddCommand,
    ]

    def activate(self, application: Application) -> None:
        """Activate plugin on poetry invokation."""
        register_commands(application=application, commands=self._commands)
        configure_azure_devops(application.poetry)
