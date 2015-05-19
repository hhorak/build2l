rpmbuild -bs --nodeps --define "_sourcedir ." --define "_srcrpmdir ." --define "dist .{{ dist_tag }}" *.spec
scp {{ package }}*.src.rpm $upload_url
pkg_url=$(get_url_smart $download_url/{{ package }}-.*.src.rpm | head -n 1)
test -z "$pkg_url" && echo "Could not get url of $download_url/{{ package }}-.*.src.rpm" && exit 1
copr-cli build {{ copr }} "$pkg_url"
