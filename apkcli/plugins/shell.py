#! /usr/bin/env python
from IPython import embed

from apkcli.plugins.base import Plugin


class PluginShell(Plugin):
    name = "shell"
    description = "Launch ipython shell to analyze the APK file"

    def add_arguments(self, parser):
        self.parser = parser

    def run(self, args, a, d, dx):
        print("Shell with androguard objects : a, d, dx")
        embed()
