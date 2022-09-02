#! /usr/bin/env python
from apkcli.plugins.base import Plugin


BLOCK_TYPES = {
    0x7109871a: 'SIGNv2',
    0xf05368c0: 'SIGNv3',
    0x2146444e: 'Google Metadata',
    0x42726577: 'Padding'
}


class PluginFrosting(Plugin):
    name = "frosting"
    description = "Check if Google Play metadata (frosting) is in the APK"

    def add_arguments(self, parser):
        self.parser = parser

    def run(self, args, a, d, dx):
        if a.is_signed_v1():
            print("V1 Signature")
        if a.is_signed_v2():
            print("V2 Signature")
        if a.is_signed_v3():
            print("V3 Signature")
        print("")
        print("Signing Blocks:")
        if len(a._v2_blocks) > 0:
            for b in a._v2_blocks:
                if b in BLOCK_TYPES.keys():
                    print("\t{}".format(BLOCK_TYPES[b]))
                else:
                    print("\tUnknown block {}".format(hex(b)))
        else:
            print("None")
