rpmdev-bumpspec -c "{{ commit_message }}" {{ package }}.spec

rhpkg clog
rhpkg commit -F clog
rhpkg push
rhpkg build
