#! /usr/bin/env python
import os
from apk.plugins.base import Plugin


def convert_x509_name(name):
    """
    Convert x509 name to a string
    """
    types = {
        'country_name': 'C',
        'state_or_province_name': 'ST',
        'locality_name': 'L',
        'organization_name': 'O',
        'organizational_unit_name': 'OU',
        'common_name': 'CN',
        'email_address': 'emailAddress'
    }

    return '/'.join(['{}={}'.format(types[attr], name.native[attr]) for attr in name.native])


class PluginCert(Plugin):
    name = "cert"
    description = "Show the certificate"

    def add_arguments(self, parser):
        self.parser = parser

    def run(self, args, apk, d, dx):
        if len(apk.get_certificates()) > 0:
            cert = apk.get_certificates()[0]
            print("SHA1: {}".format(cert.sha1_fingerprint.replace(' ', '')))
            print('Serial: {:X}'.format(cert.serial_number))
            print("Issuer: {}".format(convert_x509_name(cert.issuer)))
            print("Subject: {}".format(convert_x509_name(cert.subject)))
            print("Not Before: {}".format(cert['tbs_certificate']['validity']['not_before'].native.strftime('%b %-d %X %Y %Z')))
            print("Not After: {}".format(cert['tbs_certificate']['validity']['not_after'].native.strftime('%b %-d %X %Y %Z')))
        else:
            print("No certificate here, weird")
