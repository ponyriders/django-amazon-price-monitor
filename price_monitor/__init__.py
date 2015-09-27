"""
django-amazon-price-monitor monitors prices of Amazon products.
"""
__version_info__ = {
    'major': 0,
    'minor': 3,
    'micro': 0,
    'releaselevel': 'beta',
    'serial': 2,
}


def get_version(short=False):
    assert __version_info__['releaselevel'] in ('alpha', 'beta', 'final')
    version = ["%(major)i.%(minor)i" % __version_info__, ]
    if __version_info__['micro']:
        version.append(".%(micro)i" % __version_info__)
    if __version_info__['releaselevel'] != 'final' and not short:
        version.append('%s%i' % (__version_info__['releaselevel'][0], __version_info__['serial']))
    return ''.join(version)

__version__ = get_version()
