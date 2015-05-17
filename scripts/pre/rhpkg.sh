#TODO: make branch configureable during script generation
rhpkg clone {{ package }}
cd {{ package }}
rhpkg switch-branch {{ branch }}
