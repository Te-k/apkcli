#! /usr/bin/env python
import hashlib

from rich.console import Console

from apkcli.lib.utils import (DANGEROUS_PERMISSIONS, convert_x509_name,
                              get_urls, has_frosting)
from apkcli.plugins.base import Plugin


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
        console = Console()

        # General Information
        console.print("Metadata", style="blue")
        console.print("="*80, style="blue")
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
        console.print("Certificate", style="blue")
        console.print("="*80, style="blue")
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
            console.print("No certificate here, weird", style="red")
        print("")
        console.print("Manifest", style="blue")
        console.print("="*80, style="blue")
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
        console.print("Permissions", style="blue")
        console.print("="*80, style="blue")
        for p in sorted(apk.get_permissions()):
            if p in DANGEROUS_PERMISSIONS:
                console.print(p, style="bold red")
            else:
                print(p)

        print("")
        console.print("Urls", style="blue")
        console.print("="*80, style="blue")
        for u in sorted(get_urls(apk)):
            print(u)
