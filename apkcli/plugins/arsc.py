#! /usr/bin/env python
import sys
from apkcli.plugins.base import Plugin
from lxml import etree


class PluginArsc(Plugin):
    name = "arsc"
    description = "List strings from resource files"

    def add_arguments(self, parser):
        self.parser = parser

    def run(self, args, a, d, dx):
        arscobj = a.get_android_resources()
        if not arscobj:
            print("The APK does not contain a resources file!", file=sys.stderr)
            sys.exit(0)
        else:
            xmltree = arscobj.get_public_resources(arscobj.get_packages_names()[0])
            x = etree.fromstring(xmltree)
            for elt in x:
                if elt.get('type') == 'string':
                    _id = int(elt.get('id')[2:], 16)
                    try:
                        val = arscobj.get_resolved_res_configs(_id)[0][1]
                        print('{}\t{}\t{}'.format(
                            elt.get('id'),
                            elt.get('name'),
                            val
                        ))
                    except IndexError:
                        print("{} : Resource not found".format(elt.get('id')))
