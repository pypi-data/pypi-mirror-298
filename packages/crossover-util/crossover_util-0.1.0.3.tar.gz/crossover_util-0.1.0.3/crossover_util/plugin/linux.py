from crossover_util.plugin.plugin import CrossOverControlPlugin, Platform, Plugin


class LinuxPlugin(Plugin, CrossOverControlPlugin):
    """Plugin to manage linux specific features."""

    name = "crossover"
    platforms = [Platform.linux]
