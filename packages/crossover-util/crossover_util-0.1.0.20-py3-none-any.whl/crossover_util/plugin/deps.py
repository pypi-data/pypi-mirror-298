import importlib
import platform
import sys
import subprocess
from subprocess import STDOUT

from crossover_util.plugin.plugin import Plugin, clickable

import click


class DepsPlugin(Plugin):
    """Plugin to manage dependencies.

    \b
    Checks for missing dependencies and installs them.
    Handles adding and removing plugins.
    """

    name = "deps"

    @staticmethod
    def pip_install(*packages: str, allow_error: bool = False):
        """Install package using pip."""

        try:
            subprocess.check_output(
                [
                    "arch",
                    f"-{platform.machine()}",
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    "--user",
                    *packages,
                ],
                stderr=STDOUT,
            )
        except subprocess.CalledProcessError as e:
            if allow_error:
                return

            raise click.UsageError(e.output.decode())

    @click.argument("package")
    @clickable
    def add_extra_plugin(self, package: str):
        """Add a plugin to the list of plugins to load."""

        try:
            importlib.import_module(package)
            self.config.plugins.add(package)
            self.config.write()

            return
        except ImportError:
            pass

        if "git+" in package:
            self.pip_install(package)
            package = package.split("/")[-1].replace(".git", "")
        else:
            self.pip_install(package)

        try:
            plugins = self.find_plugins_in_module(package)
            if not plugins:
                raise click.UsageError(
                    f"Package `{package}` is not a crossover-util plugin library."
                )
        except ImportError:
            raise click.UsageError(f"Package `{package}` not found.")

        self.config.plugins.add(package)
        self.config.write()

    @click.argument("package")
    @clickable
    def remove_extra_plugin(self, package: str):
        """Remove a plugin from the list of plugins to load."""

        if package not in self.config.plugins:
            raise click.UsageError(f"Package `{package}` not found in list of plugins.")

        self.config.plugins.remove(package)
        self.config.write()

    def setup_cli(self):
        if self.config is None:
            return

        self.cli_command("add-plugin")(self.add_extra_plugin)
        self.cli_command("remove-plugin")(self.remove_extra_plugin)

    def on_load(self):
        self.ensure_plugins()
        self.setup_cli()

    def ensure_plugins(self):
        """Ensure dependencies are installed."""

        if self.config is None:
            return

        plugins_to_install = set()

        for plugin in self.config.plugins:
            try:
                importlib.import_module(plugin)
            except ImportError:
                plugins_to_install.add(plugin)

        if plugins_to_install:
            self.pip_install(*plugins_to_install, allow_error=True)
