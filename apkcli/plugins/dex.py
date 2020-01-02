#! /usr/bin/env python
import os
from apkcli.plugins.base import Plugin


class PluginDex(Plugin):
    name = "dex"
    description = "Extract the dex files"

    def add_arguments(self, parser):
        self.parser = parser

    def run(self, args, apk, d, dx):
        dex_names = list(apk.get_dex_names())
        if len(dex_names) == 0:
            print("No dex files in this APK")
        else:
            dex_values = list(apk.get_all_dex())
            for dex in range(len(dex_names)):
                dex_filename = os.path.splitext(args.APK)[0] + '.' + dex_names[dex]
                if os.path.exists(dex_filename):
                    print("{} already exist".format(dex_filename))
                else:
                    with open(dex_filename, 'wb') as f:
                        f.write(dex_values[dex])
                    print("Dex file {} created".format(dex_filename))
