import click

from crossover_util.plugin.plugin import (
    Plugin,
    clickable,
    restart_required,
    save_config,
)


class ResetPlugin(Plugin):
    """Resets all parameters to default values."""

    name = "reset"

    @clickable
    @save_config
    @restart_required
    def reset(self):
        """Reset all parameters to default values."""

        self.config.plugins_data.clear()

        click.echo("All parameters have been reset.")

    def on_load(self):
        self.cli_command("all")(self.reset)
