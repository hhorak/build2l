#!/usr/bin/python
# EASY-INSTALL-ENTRY-SCRIPT: 'build2l==0.1','console_scripts','build2l'
__requires__ = 'build2l==0.1'

import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.exit(
        load_entry_point('build2l==0.1', 'console_scripts', 'build2l')()
    )
