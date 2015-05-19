download_file_smart $get_url/{{ package }}-.*.src.rpm
rpmdev-extract {{ package }}-*.src.rpm
cd {{ package }}-*.src
