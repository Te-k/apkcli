#! /usr/bin/env python
from apkcli.plugins.base import Plugin
from apkcli.lib.utils import has_frosting, has_classnames_obfuscated


class PluginCheck(Plugin):
    name = "check"
    description = "Check for unusual stuff in the APK"

    def add_arguments(self, parser):
        self.parser = parser

    def run(self, args, apk, d, dx):
        if has_frosting(apk):
            print("APK has GooglePlay Metadata")
        if has_classnames_obfuscated(dx):
            print("Class names are obfuscated")
