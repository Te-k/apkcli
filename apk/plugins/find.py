#! /usr/bin/env python
import os
import re
from apk.plugins.base import Plugin


class PluginFind(Plugin):
    name = "find"
    description = "Find something in the APK"

    def add_arguments(self, parser):
        subparsers = parser.add_subparsers(help='Subcommand')
        parser_a = subparsers.add_parser('call', help='Find where a function is called (for instance InetAddress->getByName)')
        parser_a.add_argument('CALL', help='Function to be searched in the code')
        parser_a.add_argument('--verbose', '-v', action='store_true', help='Verbose mode')
        parser_a.set_defaults(subcommand='call')
        self.parser = parser

    def run(self, args, a, d, dx):
        if 'subcommand' in args:
            if args.subcommand == 'call':
                # Get all classes
                cc = [d for d in dx.get_classes()]
                found = False
                for c in cc:
                    # Get each method
                    for m in c.get_methods():
                        if args.verbose:
                            print("Analyzing {}.{}".format(c.name[1:-1].replace('/', '.'), m.name))
                        if not m.is_external():
                            for i in m.get_method().get_instructions():
                                if i.get_name() == 'invoke-static' and args.CALL.lower() in i.get_output().lower().replace(';', ''):
                                    print("Call found in {}.{}".format(c.name[1:-1].replace('/', '.'), m.name))
                                    found = True
                                    continue
                if not found:
                    print("function call not found")
            else:
                self.parser.print_help()
        else:
            self.parser.print_help()
