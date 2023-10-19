#! /usr/bin/env python
from apkcli.lib.utils import has_classnames_obfuscated, has_frosting
from apkcli.plugins.base import Plugin


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
        if "assets/index.android.bundle" in apk.get_files():
            if "Hermes" in apk.files["assets/index.android.bundle"]:
                print("App developed in React native with {}".format(apk.files["assets/index.android.bundle"]))
            else:
                print("App developed in React native with JavaScript code")
