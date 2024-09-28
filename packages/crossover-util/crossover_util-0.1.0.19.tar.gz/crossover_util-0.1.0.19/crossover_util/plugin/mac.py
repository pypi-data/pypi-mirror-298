import inspect
import os
import time
import webbrowser
from pathlib import Path
from typing import List

import click
from plumbum import ProcessExecutionError
from plumbum.cmd import mv, ditto, rm

from crossover_util.plugin.context import PluginContext
from crossover_util.plugin.plugin import (
    Architecture,
    CrossOverControlPlugin,
    Platform,
    Plugin,
    clickable,
    restart_required, save_config,
)


class MacPlugin(Plugin, CrossOverControlPlugin):
    """Plugin to manage macOS specific features.

    \b
    Enables AVX, AVX2, and DirectX Raytracing for Apple Silicon.
    Helps to patch Game Porting Toolkit.
    """

    name = "crossover"
    platforms = [Platform.macos]
    arch = [Architecture.arm64, Architecture.x86_64]

    GPTK_PATH = Path("/Volumes/Evaluation environment for Windows games 2.0")
    APP_PATH = Path("/Applications/CrossOver.app/Contents/MacOS")

    @property
    def is_running(self):
        return bool(self.find_pids())

    @clickable
    @restart_required
    @save_config
    def enable_avx(self):
        """Enable AVX."""

        self.data["ROSETTA_ADVERTISE_AVX"] = True

        click.echo("AVX enabled.")

    @clickable
    @restart_required
    @save_config
    def enable_dxr(self):
        """Enable DirectX Raytracing."""

        self.data["D3DM_SUPPORT_DXR"] = True

        click.echo("DirectX Raytracing enabled.")

    @clickable
    @restart_required
    @save_config
    def disable_avx(self):
        """Disable AVX."""

        self.data["ROSETTA_ADVERTISE_AVX"] = False

        click.echo("AVX disabled.")

    @clickable
    @restart_required
    @save_config
    def disable_dxr(self):
        """Disable DirectX Raytracing."""

        self.data["D3DM_SUPPORT_DXR"] = False

        click.echo("DirectX Raytracing disabled.")

    @clickable
    def patch_gptk(self):
        """Patch Game Porting Toolkit."""

        if not self.GPTK_PATH.exists():
            click.echo("Mounted GPTK not found.")
            click.echo("Please download Game Porting Toolkit from Apple's website.")
            click.echo("Mount downloaded disk image.")
            click.echo(
                "Then mount `Evaluation environment` and call this command again."
            )

            if click.confirm("Would you like to download GPTK?", abort=True):
                webbrowser.open(
                    "https://developer.apple.com/games/game-porting-toolkit/"
                )
            return

        crossover_gptk_path = Path(
            "/Applications/CrossOver.app/Contents/SharedSupport/CrossOver"
            "/lib64/apple_gptk/external"
        )

        if not os.path.exists(crossover_gptk_path):
            os.makedirs(crossover_gptk_path)

        rm["-rf", crossover_gptk_path.joinpath("D3DMetal.framework-old")]()
        rm["-rf", crossover_gptk_path.joinpath("libd3dshared.dylib-old")]()

        mv[
            crossover_gptk_path.joinpath("D3DMetal.framework"),
            crossover_gptk_path.joinpath("D3DMetal.framework-old"),
        ]()

        mv[
            crossover_gptk_path.joinpath("libd3dshared.dylib"),
            crossover_gptk_path.joinpath("libd3dshared.dylib-old"),
        ]()

        ditto[self.GPTK_PATH.joinpath("redist/lib/external"), crossover_gptk_path]()

        click.echo("GPTK patched")

    def on_load(self):
        self.cli_command("enable-avx")(self.enable_avx)
        self.cli_command("enable-dxr")(self.enable_dxr)
        self.cli_command("disable-avx")(self.disable_avx)
        self.cli_command("disable-dxr")(self.disable_dxr)
        self.cli_command("patch-gptk")(self.patch_gptk)

    def on_start(self, ctx: PluginContext):
        if self.data.get("ROSETTA_ADVERTISE_AVX"):
            ctx.environment["ROSETTA_ADVERTISE_AVX"] = "1"

        if self.data.get("D3DM_SUPPORT_DXR"):
            ctx.environment["D3DM_SUPPORT_DXR"] = "1"

    def find_pids(self) -> List[int]:
        """Find the PIDs of the CrossOver processes."""

        from plumbum.cmd import ps, grep

        pids = ps["-A"] | grep[self.APP_PATH]

        return [
            int(row.split()[0])
            for row in pids().strip().split("\n")
            if "grep" not in row.split()[3] and int(row.split()[0]) != os.getpid()
        ]

    def kill_crossover(self, silent: bool = False) -> None:
        """Kill the CrossOver processes."""

        from plumbum.cmd import kill

        crossover_pids = self.find_pids()

        if crossover_pids and not silent:
            click.echo("CrossOver is running. Terminating...")

        for pid in self.find_pids():
            try:
                kill["-15"](pid)
            except ProcessExecutionError:
                pass

        while self.find_pids():
            time.sleep(0.2)
        else:
            if not silent:
                click.echo("CrossOver has been terminated.")

    def run_crossover(self, background: bool = False):
        """Run CrossOver."""

        from plumbum.cmd import zsh

        ctx = PluginContext()

        for plugin in Plugin.all_plugins():
            plugin.on_start(ctx)

        bin_path = self.APP_PATH.joinpath("CrossOver")

        if self.APP_PATH.joinpath("CrossOver.origin").exists():
            bin_path = self.APP_PATH.joinpath("CrossOver.origin")

        cmd = zsh["-c"][f"{ctx.env_str} {bin_path.expanduser()} {ctx.args_str}"]

        if background:
            cmd.nohup()
        else:
            cmd()

    def install(self):
        """Inject self as the CrossOver process."""

        from plumbum.cmd import chmod

        self.kill_crossover(silent=True)

        bin_path = self.APP_PATH.joinpath("CrossOver")

        if not self.APP_PATH.joinpath("CrossOver.origin").exists():
            mv[bin_path, bin_path.with_suffix(".origin")]()
        else:
            click.echo("CrossOver is already injected. Updating...")

        entrypoint = inspect.cleandoc(
            """
                #!/usr/bin/env python3
                import syslog
                import logging
                import sys
                import platform
                import subprocess
                import importlib

                syslog.openlog("CrossOverUtil")
                logging.basicConfig(filename="/tmp/crossover-util.log", level=logging.DEBUG)

                try:
                    importlib.import_module("crossover_util")
                except ImportError:
                    subprocess.check_output(
                        [
                            "arch", f"-{platform.machine()}", 
                            sys.executable, "-m", "pip", "install", "--user", "--upgrade",
                            "--ignore-installed",
                            "crossover-util"
                        ]
                    )

                try:
                    import crossover_util
                    from crossover_util.config import config   
                except Exception as e:
                    syslog.syslog(syslog.LOG_ALERT, str(e))
                    logging.exception("Failed to initialize CrossOverUtil.")
                    sys.exit(1)

                config.init_plugins()

                if __name__ == "__main__":
                    try:
                        sys.exit(config.crossover_plugin.run_crossover())
                    except Exception as e:
                        syslog.syslog(syslog.LOG_ALERT, str(e))
                        logging.exception("Failed to run CrossOver.")
                        sys.exit(1)
            """
        )

        with open(bin_path, "w") as entrypoint_file:
            entrypoint_file.write(entrypoint)

        chmod["+x"](bin_path)
        chmod["+x"](bin_path.with_suffix(".origin"))

        click.echo("CrossOver patch has been injected.")

    def uninstall(self):
        self.kill_crossover(silent=True)

        bin_path = self.APP_PATH.joinpath("CrossOver")

        if self.APP_PATH.joinpath("CrossOver.origin").exists():
            mv[bin_path.with_suffix(".origin"), bin_path]()
            click.echo("CrossOver has been restored.")
