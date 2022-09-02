#! /usr/bin/env python
import re
from apkcli.plugins.base import Plugin
from lxml import etree


class PluginEnum(Plugin):
    name = "enum"
    description = "Enumerate interesting informations"

    def add_arguments(self, parser):
        self.parser = parser
        self.uri_regex = br"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
        self.ip_regex = br"(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])(?<!172\.(16|17|18|19|20|21|22|23|24|25|26|27|28|29|30|31))(?<!127)(?<!^10)(?<!^0)\.([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])(?<!192\.168)(?<!172\.(16|17|18|19|20|21|22|23|24|25|26|27|28|29|30|31))\.([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])(?<!\.255$))"  # noqa: E501
        # Inspired by https://github.com/shivsahni/APKEnum/blob/master/APKEnum.py
        self.s3_regexes = [
            rb"https*://(.+?)\.s3\..+?\.amazonaws\.com\/.+?",
            rb"https*://s3\..+?\.amazonaws\.com\/(.+?)\/.+?",
            rb"https*://(.+?)\.s3-website\..+?\.amazonaws\.com",
            rb"https*://(.+?)\.s3-website-.+?\.amazonaws\.com"
        ]

    def get_urls(self, a):
        res = []
        for dex in a.get_all_dex():
            res += re.findall(self.uri_regex, dex)
        return res

    def get_ips(self, a):
        res = []
        for dex in a.get_all_dex():
            res += [b[0] for b in re.findall(self.ip_regex, dex)]
        return res

    def get_s3(self, a):
        res = []
        for dex in a.get_all_dex():
            for regex in self.s3_regexes:
                res += re.findall(regex, dex)
        return res

    def get_firebase(self, a):
        arscobj = a.get_android_resources()
        if not arscobj:
            return None
        xmltree = arscobj.get_public_resources(arscobj.get_packages_names()[0])
        x = etree.fromstring(xmltree)
        for elt in x:
            if elt.get('type') == 'string':
                val = arscobj.get_resolved_res_configs(int(elt.get('id')[2:], 16))[0][1]
                if val.endswith('firebaseio.com'):
                    return val
        return None

    def run(self, args, a, d, dx):
        dex_values = list(a.get_all_dex())
        print("-------------------- urls ----------------------")
        if len(dex_values) == 0:
            print("No DEX files")
        else:
            res = self.get_urls(a)
            if len(res) > 0:
                for s in res:
                    print(s.decode('utf-8'))
            else:
                print("No url found")
        print("")
        print("-------------------- IPs ------------------------")
        if len(dex_values) == 0:
            print("No DEX files")
        else:
            res = self.get_ips(a)
            if len(res) > 0:
                for s in res:
                    print(s.decode('utf-8'))
            else:
                print("No IP found")
        print("")
        print("----------------------- S3 ---------------------")
        if len(dex_values) == 0:
            print("No DEX files")
        else:
            res = self.get_s3(a)
            if len(res) > 0:
                for s in res:
                    print(s.decode('utf-8'))
            else:
                print("No S3 bucket found")
        print("")
        print("----------------------- FireBase ---------------------")
        firebase_url = self.get_firebase(a)
        if firebase_url:
            print(firebase_url)
        else:
            print("Not found")
