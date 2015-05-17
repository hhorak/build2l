rpmbuild -bs --nodeps --define "_sourcedir ." --define "_srcrpmdir ." --define "dist .{{ dist_tag }}" *.spec
mock -r {{ mock_config }} --rebuild *.src.rpm
