#! /usr/bin/env python
from apkcli.plugins.base import Plugin
from IPython import embed


class PluginShell(Plugin):
    name = "shell"
    description = "Launch ipython shell to analyze the APK file"

    def add_arguments(self, parser):
        self.parser = parser

    def run(self, args, a, d, dx):
        print("Shell with androguard objects : a, d, dx")
        embed()
