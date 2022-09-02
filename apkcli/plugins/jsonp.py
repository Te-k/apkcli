#! /usr/bin/env python
import hashlib
import json
from apkcli.plugins.base import Plugin
from apkcli.lib.utils import get_urls, get_intent_filers, convert_x509_name


class PluginJson(Plugin):
    name = "json"
    description = "Extract information on the APK in JSON format"

    def add_arguments(self, parser):
        self.parser = parser

    def extract_new_permissions(self, permissions):
        """
        Extract permissions that are not default in Android
        """
        res = []
        for p in permissions:
            if p.startswith('android.permission'):
                continue
            if p.startswith('com.google'):
                continue
            if p.startswith('com.android'):
                continue
            res.append(p)
        return res

    def run(self, args, apk, d, dx):
        res = {
            'app_name': apk.get_app_name(),
            'package_name': apk.get_package(),
            'providers': apk.get_providers(),
            'new_permissions': self.extract_new_permissions(apk.get_permissions()),
            'filters': get_intent_filers(apk),
            'certificate': {},
            'wearable': apk.is_wearable(),
            'max_sdk_version': (apk.get_max_sdk_version()),
            'min_sdk_version': int(apk.get_min_sdk_version()) if apk.get_min_sdk_version() is not None else "",
            'version_code': apk.xml['AndroidManifest.xml'].get('{http://schemas.android.com/apk/res/android}versionCode'),
            'libraries': list(apk.get_libraries()),
            'androidtv': apk.is_androidtv(),
            'target_sdk_version': apk.get_target_sdk_version(),
            'activities': apk.get_activities(),
            'main_activity': apk.get_main_activity(),
            'receivers': apk.get_receivers(),
            'signature_name': apk.get_signature_name(),
            'dexes': {},
            'displayed_version': apk.xml['AndroidManifest.xml'].get('{http://schemas.android.com/apk/res/android}versionName'),
            'services': apk.get_services(),
            'permissions': apk.get_permissions(),
            'urls': get_urls(apk),
        }

        # Certificate
        if len(apk.get_certificates()) > 0:
            cert = apk.get_certificates()[0]
            res['certificate']['sha1'] = cert.sha1_fingerprint.replace(' ', '')
            res['certificate']['serial'] = '{:X}'.format(cert.serial_number)
            res['certificate']['issuerDN'] = convert_x509_name(cert.issuer)
            res['certificate']['subjectDN'] = convert_x509_name(cert.subject)
            res['certificate']['not_before'] = cert['tbs_certificate']['validity']['not_before'].native.strftime('%b %-d %X %Y %Z')
            res['certificate']['not_after'] = cert['tbs_certificate']['validity']['not_after'].native.strftime('%b %-d %X %Y %Z')

        # Dexes
        dex_names = list(apk.get_dex_names())
        dex_values = list(apk.get_all_dex())
        for dex in range(len(dex_names)):
            m = hashlib.sha256()
            m.update(dex_values[dex])
            res['dexes'][dex_names[dex][:-4]] = {
                'sha256': m.hexdigest(),
            }

        print(json.dumps(res, indent=4, sort_keys=True))
