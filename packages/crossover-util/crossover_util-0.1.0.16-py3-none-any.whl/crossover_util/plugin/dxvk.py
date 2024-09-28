import click

from crossover_util.plugin.plugin import Plugin, clickable, restart_required
from crossover_util.plugin.context import PluginContext


class DXVKPlugin(Plugin):
    """Plugin to manage DXVK."""

    name = "dxvk"

    @property
    def async_enabled(self):
        return self.data.get("async", False)

    @clickable
    @restart_required
    def enable_async(self):
        """Enable async compute."""

        self.data["async"] = True

        click.echo("Async compute enabled.")

    @clickable
    @restart_required
    def disable_async(self):
        """Disable async compute."""

        self.data.pop("async", None)

        click.echo("Async compute disabled.")

    def on_load(self):
        self.cli_command("enable-async")(self.enable_async)
        self.cli_command("disable-async")(self.disable_async)

    def on_start(self, ctx: "PluginContext"):
        if self.async_enabled:
            ctx.environment["DXVK_ASYNC"] = "1"
