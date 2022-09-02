#! /usr/bin/env python
import re
from apkcli.plugins.base import Plugin


class PluginFind(Plugin):
    name = "find"
    description = "Find something in the APK"

    def add_arguments(self, parser):
        subparsers = parser.add_subparsers(help='Subcommand')
        parser_a = subparsers.add_parser('call', help='Find where a function is called (for instance InetAddress->getByName)')
        parser_a.add_argument('CALL', help='Call to be searched in the code')
        parser_a.add_argument('--verbose', '-v', action='store_true', help='Verbose mode')
        parser_a.set_defaults(subcommand='call')
        parser_b = subparsers.add_parser('function', help='Find all the functions with a specific name')
        parser_b.add_argument('NAME', help='Function to be searched in the code')
        parser_b.add_argument('--regex', '-R', action='store_true', help='Regex query')
        parser_b.add_argument('--verbose', '-v', action='store_true', help='Verbose mode')
        parser_b.set_defaults(subcommand='function')
        parser_c = subparsers.add_parser('string', help='Find a string used in the source code')
        parser_c.add_argument('STRING', help='String to be searched in the code')
        parser_c.add_argument('--regex', '-R', action='store_true', help='Regex query')
        parser_c.set_defaults(subcommand='string')
        self.parser = parser

    def run(self, args, a, d, dx):
        if 'subcommand' in args:
            if args.subcommand == 'call':
                # Get all classes
                found = False
                for c in dx.get_classes():
                    # Get each method
                    for m in c.get_methods():
                        if args.verbose:
                            print("Analyzing {}.{}".format(c.name[1:-1].replace('/', '.'), m.name))
                        if not m.is_external():
                            for i in m.get_method().get_instructions():
                                if i.get_name() in ['invoke-static', 'invoke-virtual'] and args.CALL.lower() in i.get_output().lower().replace(';', ''):
                                    print("Call found in {}.{}".format(c.name[1:-1].replace('/', '.'), m.name))
                                    found = True
                if not found:
                    print("function call not found")
            elif args.subcommand == 'function':
                found = False
                for c in dx.get_classes():
                    if args.verbose:
                        print("Checking {}".format(c.name[1:-1].replace('/', '.')))
                    for m in c.get_methods():
                        if args.regex:
                            if re.match(args.NAME, m.name):
                                print("Function found {}.{}".format(c.name[1:-1].replace('/', '.'), m.name))
                                found = True
                        else:
                            if args.NAME.lower() in m.name.lower():
                                print("Function found {}.{}".format(c.name[1:-1].replace('/', '.'), m.name))
                                found = True
                if not found:
                    print("Not found")
            elif args.subcommand == 'string':
                found = False
                for c in dx.get_classes():
                    # Search in global fields
                    for f in c.get_fields():
                        if f.get_field().get_descriptor() == 'Ljava/lang/String;':
                            if f.get_field().get_init_value():
                                if f.get_field().get_init_value().get_value():
                                    if args.regex:
                                        if re.match(args.STRING, f.get_field().get_init_value().get_value()):
                                            print("String found as the field {} of the class {}".format(f.name, c.name[1:-1].replace('/', '.')))
                                            found = True
                                    else:
                                        if args.STRING.lower() in f.get_field().get_init_value().get_value().lower():
                                            print("String found as the field {} of the class {}".format(f.name, c.name[1:-1].replace('/', '.')))
                                            found = True
                    # Search in methods as constants
                    for m in c.get_methods():
                        if not m.is_external():
                            _i = 0
                            for i in m.get_method().get_instructions():
                                if i.get_name() == 'const-string':
                                    if args.regex:
                                        if re.match(args.STRING, i.get_raw_string()):
                                            print("String found at {}.{} instruction {}".format(
                                                c.name[1:-1].replace('/', '.'),
                                                m.name,
                                                _i
                                            ))
                                            found = True
                                    else:
                                        if args.STRING.lower() in i.get_raw_string().lower():
                                            print("String found at {}.{} instruction {}".format(
                                                c.name[1:-1].replace('/', '.'),
                                                m.name,
                                                _i
                                            ))
                                            found = True
                                _i += 1
                if not found:
                    print("Not found")
            else:
                self.parser.print_help()
        else:
            self.parser.print_help()
