import re


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


def has_frosting(apk):
    """
    Detect if Google Play metadata is in the APK
    """
    # Parse signatures
    apk.parse_v2_v3_signature()
    return (0x2146444e in apk._v2_blocks)


def get_urls(apk):
    """
    Extract urls from data
    """
    res = []
    for dex in apk.get_all_dex():
        res += re.findall(br"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", dex)
    return [s.decode('utf-8') for s in res]


def get_intent_filers(apk):
    """
    Extract all intent filters from the Manifest
    """
    # FIXME : not sure this fully reproduce Koodous filters
    res = []
    filters = apk.xml['AndroidManifest.xml'].findall(".//intent-filter")
    for f in filters:
        for ff in f.findall('.//action'):
            filt = ff.get('{http://schemas.android.com/apk/res/android}name')
            if filt:
                res.append(filt)
    return res


def has_classnames_obfuscated(dx):
    """
    Check if the APK has the class names obfuscated
    Count the number of classes with a name of one character
    Returns True of more than 50% of classes have names of 1 char
    """
    cn = [c.name[1:-1].split('/') for c in dx.get_classes()]
    cnn = [len(a.split('$')[0]) for b in cn for a in b]
    return (cnn.count(1) / len(cnn)) > 0.5
