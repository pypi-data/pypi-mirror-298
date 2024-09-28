# CrossOver-Util

This is a collection of utility functions that I have written over the years. I have decided to put them all in one place so that I can easily access them. I have also included a few utility functions that I have found useful from other sources.

## Installation

```bash
pip install --user crossover-util
```

## Usage

```zsh
crossover-util install
```

## Write your own plugin

You can add your own plugin that performs a specific task. To do this, you need to create a new Python file in the `plugins` directory. The file should contain a class that inherits from the `Plugin` class. 

To add click command use the 

```python
import click

from crossover_util.plugin.plugin import Plugin, clickable
from crossover_util.plugin.context import PluginContext


class MyPlugin(Plugin):
    name = "my-plugin"

    @clickable
    def hello(self):
        click.echo("Hello, World!")
    
    def on_load(self):
        """This method is called when the plugin is loaded.
            
        Here you can add any initialization code that you need.
        """

        self.cli_command("hello")(self.hello)

    def on_start(self, ctx: PluginContext):
        """This method is called when the CrossOver app is started.

        Here you can add env variables and arguments to CrossOver app.
        """

        ctx.environment["HELLO"] = "WORLD"
```

To access `hello` click subcommand command use the following command

```zsh
crossover-util plugin my-plugin hello
```
