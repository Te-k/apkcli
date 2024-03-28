#! /usr/bin/env python
from hexdump import hexdump

from apkcli.plugins.base import Plugin


class PluginFunction(Plugin):
    name = "func"
    description = "Provides details on a function"

    def add_arguments(self, parser):
        parser.add_argument('CLASS', help="class name (like com/google/something)")
        parser.add_argument('METHOD', help="method name")
        self.parser = parser

    def run(self, args, a, d, dx):
        methods = [m for m in dx.get_methods() if args.CLASS in m.class_name and m.name == args.METHOD]
        if len(methods) == 0:
            print("Method not found")
            return

        for m in methods:
            mm = m.get_method()
            print("Method found : {} - {}".format(m.class_name, m.name))
            print(m.full_name)
            print("")
            print(m.show())
            print("")
            print(mm.show())
            if mm.get_code():
                print("")
                print(hexdump(mm.get_code().get_bc().get_raw()))
