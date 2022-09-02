#! /usr/bin/env python
import re
from apkcli.plugins.base import Plugin


class PluginUrls(Plugin):
    name = "urls"
    description = "Extract URLs from the DEX files"

    def add_arguments(self, parser):
        self.parser = parser

    def run(self, args, a, d, dx):
        dex_values = list(a.get_all_dex())
        if len(dex_values) == 0:
            print("No DEX files")
        else:
            res = []
            for dex in a.get_all_dex():
                res += re.findall(br"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", dex)
            if len(res) > 0:
                for s in res:
                    print(s.decode('utf-8'))
            else:
                print("No url found")
