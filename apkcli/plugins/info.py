#! /usr/bin/env python
import hashlib
from apkcli.plugins.base import Plugin
from apkcli.lib.utils import convert_x509_name, has_frosting, get_urls


class PluginInfo(Plugin):
    name = "info"
    description = "Show the certificate"

    def add_arguments(self, parser):
        self.parser = parser

    def display_hashes(self, data):
        """Display md5, sha1 and sh256 of the data given"""
        for algo in ["md5", "sha1", "sha256"]:
            m = getattr(hashlib, algo)()
            m.update(data)
            print("%-15s %s" % (algo.upper()+":", m.hexdigest()))

    def run(self, args, apk, d, dx):
        # General Information
        print("Metadata")
        print("="*80)
        with open(args.APK, 'rb') as f:
            self.display_hashes(f.read())
        print("{:15} {}".format("Package Name:", apk.get_package()))
        if apk.get_app_name().strip() != '':
            print("{:15} {}".format("App:", apk.get_app_name()))
        if has_frosting(apk):
            print("This APK has Google Play metadata")
        if len(list(apk.get_dex_names())) == 0:
            print("This APK does not have any DEX file")
        print("")

        # Certificate
        print("Certificate")
        print("="*80)
        if len(apk.get_certificates()) > 0:
            cert = apk.get_certificates()[0]
            print("{:15} {}".format("SHA1:", cert.sha1_fingerprint.replace(' ', '')))
            print('{:15} {:X}'.format("Serial:", cert.serial_number))
            print("{:15} {}".format("Issuer:", convert_x509_name(cert.issuer)))
            print("{:15} {}".format("Subject:", convert_x509_name(cert.subject)))
            print("{:15} {}".format(
                "Not Before:",
                cert['tbs_certificate']['validity']['not_before'].native.strftime('%b %-d %X %Y %Z')))
            print("{:15} {}".format(
                "Not After:",
                cert['tbs_certificate']['validity']['not_after'].native.strftime('%b %-d %X %Y %Z')))
        else:
            print("No certificate here, weird")
        print("")
        print("Manifest")
        print("="*80)
        if apk.get_main_activity():
            print("Main Activity: {}".format(apk.get_main_activity()))
        if len(apk.get_services()) > 0:
            print("Services:")
            for s in apk.get_services():
                print("- " + s)
        if len(apk.get_receivers()) > 0:
            print("Receivers:")
            for r in apk.get_receivers():
                print("- " + r)

        print("")
        print("Permissions")
        print("="*80)
        for p in apk.get_permissions():
            print(p)

        print("")
        print("Urls")
        print("="*80)
        for u in get_urls(apk):
            print(u)
