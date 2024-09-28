import click

from crossover_util.plugin.plugin import Plugin, clickable, restart_required, save_config
from crossover_util.plugin.context import PluginContext


class FastMathPlugin(Plugin):
    """Plugin to manage fast math."""

    name = "fastmath"

    @property
    def enabled(self):
        return self.data.get("enabled", False)

    @clickable
    @restart_required
    @save_config
    def enable(self):
        """Enable fast math."""

        self.data["enabled"] = True

        click.echo("Fast math enabled.")

    @clickable
    @restart_required
    @save_config
    def disable(self):
        """Disable fast math."""

        self.data["enabled"] = False

        click.echo("Fast math disabled.")

    def on_load(self):
        self.cli_command("enable")(self.enable)
        self.cli_command("disable")(self.disable)

    def on_start(self, ctx: "PluginContext"):
        if self.enabled:
            ctx.environment["MVK_CONFIG_FAST_MATH_ENABLED"] = "1"
