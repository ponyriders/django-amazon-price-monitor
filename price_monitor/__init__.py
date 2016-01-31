"""
django-amazon-price-monitor monitors prices of Amazon products.
"""
__version_info__ = {
    'major': 0,
    'minor': 6,
    'micro': 1,
    'releaselevel': 'final',
    'serial': 0,
}


def get_version(short=False):
    assert __version_info__['releaselevel'] in ('alpha', 'beta', 'final')
    version = ["{major:d}.{minor:d}".format(**__version_info__), ]
    if __version_info__['micro']:
        version.append(".{micro:d}".format(**__version_info__))
    if __version_info__['releaselevel'] != 'final' and not short:
        version.append('{0!s}{1:d}'.format(__version_info__['releaselevel'][0], __version_info__['serial']))
    return ''.join(version)

__version__ = get_version()
