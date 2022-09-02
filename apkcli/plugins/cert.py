#! /usr/bin/env python
from apkcli.plugins.base import Plugin
from apkcli.lib.utils import convert_x509_name


class PluginCert(Plugin):
    name = "cert"
    description = "Show the certificate"

    def add_arguments(self, parser):
        self.parser = parser

    def run(self, args, apk, d, dx):
        if len(apk.get_certificates()) > 0:
            cert = apk.get_certificates()[0]
            print("{:15}{}".format("SHA1:", cert.sha1_fingerprint.replace(' ', '')))
            print('{:15}{:X}'.format("Serial:", cert.serial_number))
            print("{:15}{}".format("Issuer:", convert_x509_name(cert.issuer)))
            print("{:15}{}".format("Subject:", convert_x509_name(cert.subject)))
            print("{:15}{}".format(
                "Not Before:",
                cert['tbs_certificate']['validity']['not_before'].native.strftime('%b %-d %X %Y %Z')))
            print("{:15}{}".format(
                "Not After:",
                cert['tbs_certificate']['validity']['not_after'].native.strftime('%b %-d %X %Y %Z')))
        else:
            print("No certificate here, weird")
