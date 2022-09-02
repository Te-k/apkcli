#! /usr/bin/env python
import re
from apkcli.plugins.base import Plugin


class PluginStrings(Plugin):
    name = "strings"
    description = "Extract strings from the DEX files"

    def strings(self, data):
        # Inspired by https://github.com/Neo23x0/yarGen/blob/master/yarGen.py
        strings_full = re.findall(b"[\x1f-\x7e]{6,}", data)
        strings_wide = re.findall(b"(?:[\x1f-\x7e][\x00]){6,}", data)
        return strings_full, strings_wide

    def add_arguments(self, parser):
        self.parser = parser

    def run(self, args, a, d, dx):
        strings = []
        dex_values = list(a.get_all_dex())
        if len(dex_values) == 0:
            print("No DEX files")
        else:
            for d in dex_values:
                f, w = self.strings(d)
                strings += f
                strings += w

            for s in strings:
                print(s.decode('utf-8', 'ignore'))
