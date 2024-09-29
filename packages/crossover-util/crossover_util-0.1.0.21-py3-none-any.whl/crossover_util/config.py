from pathlib import Path
from typing import Any, ClassVar, Dict, Set

import click
from click import Group
from pydantic import BaseModel, Field

from crossover_util.plugin.plugin import Plugin
from crossover_util.plugin.reset import ResetPlugin


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
        from crossover_util.plugin.dxvk import DXVKPlugin
        from crossover_util.plugin.fastmath import FastMathPlugin
        from crossover_util.plugin.linux import LinuxPlugin
        from crossover_util.plugin.mac import MacPlugin
        from crossover_util.plugin.plist import PListPlugin
        from crossover_util.plugin.plugin import Plugin
        from crossover_util.plugin.ue4 import UE4Plugin

        Plugin.add_plugin(DepsPlugin(self))  # Ensure deps are installed

        builtin_plugins = [
            MacPlugin,
            LinuxPlugin,
            DXVKPlugin,
            FastMathPlugin,
            UE4Plugin,
            PListPlugin,
            ResetPlugin,
        ]

        for plugin in builtin_plugins:
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

        return cls.model_validate_json(data)

    def write(self):
        """Write the config to disk."""

        config_path = Path("~/.crossover_util/config.json").expanduser()

        if not config_path.parent.exists():
            config_path.parent.mkdir(parents=True)

        with open(config_path, "w") as file:
            file.write(self.model_dump_json(by_alias=True))

    def get_plugin_data(self, plugin: "Plugin") -> Dict[str, Any]:
        self.plugins_data.setdefault(plugin.name, {})

        return self.plugins_data[plugin.name]


config = UtilConfig.read()
