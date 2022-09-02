#! /usr/bin/env python
from apkcli.plugins.base import Plugin


class PluginManifest(Plugin):
    name = "manifest"
    description = "Show the manifest"

    def add_arguments(self, parser):
        self.parser = parser

    def run(self, args, a, d, dx):
        # TODO : beautify XML here
        print(a.get_android_manifest_axml().get_xml().decode('utf-8'))
