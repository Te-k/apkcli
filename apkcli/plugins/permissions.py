#! /usr/bin/env python
from apkcli.plugins.base import Plugin


class PluginPermissions(Plugin):
    name = "permissions"
    description = "List the permissions required by the app"

    def add_arguments(self, parser):
        self.parser = parser

    def run(self, args, a, d, dx):
        perms = a.get_permissions()
        if len(perms) > 0:
            for p in a.get_permissions():
                print(p)
        else:
            print("No permissions required by this app")
