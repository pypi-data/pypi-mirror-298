import click

from crossover_util.plugin.plugin import (
    Plugin,
    clickable,
    restart_required,
    save_config,
)


class UE4Plugin(Plugin):
    """Plugin to manage UE4 compatibility."""

    name = "ue4"

    @property
    def disabled(self):
        return self.data.get("disabled", False)

    @clickable
    @restart_required
    @save_config
    def enable(self):
        """Enable UE4 compatibility."""

        self.data.pop("disabled", None)

        click.echo("UE4 compatibility enabled.")

    @clickable
    @restart_required
    @save_config
    def disable(self):
        """Disable UE4 compatibility."""

        self.data["disabled"] = True

        click.echo("UE4 compatibility disabled.")

    def on_load(self):
        self.cli_command("enable")(self.enable)
        self.cli_command("disable")(self.disable)

    def on_start(self, ctx):
        if self.disabled:
            ctx.environment["NAS_DISABLE_UE4_HACK"] = "1"
