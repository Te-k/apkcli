#! /usr/bin/env python
import yara
from apkcli.plugins.base import Plugin


class PluginYara(Plugin):
    name = "yara"
    description = "Run a Yara run on the Dex file"

    def add_arguments(self, parser):
        parser.add_argument("YARARULE", help="Path of the yara rule file")
        self.parser = parser

    def run(self, args, a, d, dx):
        rules = yara.compile(filepath=args.YARARULE)
        match = False
        for d in a.get_all_dex():
            res = rules.match(data=d)
            print(res)
            if len(res) > 0:
                for r in res:
                    print("Matches {}".format(r))
                match = True
        if not match:
            print("No match")
