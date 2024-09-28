from crossover_util.plugin.plugin import Plugin, clickable
from crossover_util.plugin.context import PluginContext


class FastMathPlugin(Plugin):
    name = "fastmath"

    @property
    def enabled(self):
        return self.data.get("enabled", False)

    @clickable
    def enable(self):
        """Enable fast math."""
        self.data["enabled"] = True

    @clickable
    def disable(self):
        """Disable fast math."""
        self.data["enabled"] = False

    def on_load(self):
        self.cli_command("enable")(self.enable)
        self.cli_command("disable")(self.disable)

    def on_start(self, ctx: "PluginContext"):
        if self.enabled:
            ctx.environment["MVK_CONFIG_FAST_MATH_ENABLED"] = "1"
