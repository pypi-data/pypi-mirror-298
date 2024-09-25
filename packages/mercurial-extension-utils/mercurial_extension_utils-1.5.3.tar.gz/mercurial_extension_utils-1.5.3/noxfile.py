import nox
import pathlib

###########################################################################
# WARNING
#
# to handle 2.7 one must be careful to use virtualenv<20.22.0,
# otherwise
#   „nox RuntimeError: failed to find interpreter for Builtin discover of python_spec='python2.7'”
# errors appear.
#
# Easiest way:
#    pipx install nox
#    pipx inject nox 'virtualenv<20.22.0'
###########################################################################


# Tested versions. Python → list of mercurials
TESTED = {
    '2.7': [
        '3.4', '3.8', '4.1', '4.9', '5.0', '5.5', '5.9',
    ],
    '3.8': [
        '5.0', '5.9',
    ],
    '3.10': [
        '5.5', '5.9', '6.1', '6.4', '6.7', '6.8',
    ],
    '3.12': [
        '6.5', '6.7', '6.8',
    ]
}

###########################################################################

nox.options.envdir = pathlib.Path.home() / ".nox_venvs" / "mercurial_exts"
nox.options.reuse_venv = True

###########################################################################

def _hgver_to_clause(ver):
    ver_items = ver.split('.')
    result = "Mercurial>={0}.{1},<{0}.{2}".format(
        ver_items[0], ver_items[1], int(ver_items[1]) + 1)
    return result


@nox.session
@nox.parametrize('python,hgver', [
    (pyver, hgver)
    for pyver in TESTED
    for hgver in TESTED[pyver]
])
def tests(session, hgver):
    if not session.python.startswith('2.') and hgver.startswith('5.'):
        session.env['HGPYTHON3'] = '1'
    session.env['HGRCPATH'] = '/dev/null'

    if session.python in ['3.4']:
        session.install('doctest')

    session.install(_hgver_to_clause(hgver))
    session.install('.')
    session.run('python', '-m', 'unittest', 'discover', 'tests')
