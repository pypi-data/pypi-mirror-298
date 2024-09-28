from pathlib import Path
from typing import Any, ClassVar, Dict, Set

import click
from click import Group
from pydantic import BaseModel, Field

from crossover_util.plugin.linux import LinuxPlugin
from crossover_util.plugin.plugin import Plugin


class UtilConfig(BaseModel):
    plugins: Set[str] = Field(
        default_factory=set, description="List of plugins to load"
    )

    plugins_data: Dict[str, Any] = Field(
        default_factory=dict, description="Plugins Data"
    )

    CONFIG_PATH: ClassVar[Path] = Path("~/.crossover_util/config.json").expanduser()
    PLUGIN_CLI: ClassVar[Group] = Group("plugin")

    @property
    def plugin_cli(self):
        return self.PLUGIN_CLI

    @property
    def crossover_plugin(self):
        plugin = Plugin.get_plugin("crossover")
        if plugin is None:
            raise click.UsageError("Unsupported platform.")
        return plugin

    def init_plugins(self):
        from crossover_util.plugin.deps import DepsPlugin
        from crossover_util.plugin.plugin import Plugin

        Plugin.add_plugin(DepsPlugin(self))  # Ensure deps are installed

        from crossover_util.plugin.mac import MacPlugin

        for plugin in [MacPlugin, LinuxPlugin]:
            Plugin.add_plugin(plugin(self))

        for plugin_module in self.plugins:
            Plugin.import_plugins(plugin_module, self)

        for plugin in Plugin.all_plugins():
            plugin.on_load()

    @classmethod
    def read(cls) -> "UtilConfig":
        try:
            with open(cls.CONFIG_PATH, "r") as file:
                data = file.read() or "{}"
        except FileNotFoundError:
            data = "{}"

        return cls.parse_raw(data)

    def write(self):
        """Write the config to disk."""

        config_path = Path("~/.crossover_util/config.json").expanduser()

        if not config_path.parent.exists():
            config_path.parent.mkdir(parents=True)

        with open(config_path, "w") as file:
            file.write(self.json(by_alias=True))

    def get_plugin_data(self, plugin: "Plugin") -> Dict[str, Any]:
        self.plugins_data.setdefault(plugin.name, {})

        return self.plugins_data[plugin.name]


config = UtilConfig.read()
