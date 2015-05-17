build2l
=======

Tool to (re)build set of packages.

It gets YAML file where a recipe to rebuild set of packages is described.
Based on that file a scenario script is generated and with running the scenario
script a user may rebuild the set of tables.

The tool doesn't do anything and the responsibility is always on the user
that runs the scenario script.

Usage
-----
First we need a YAML config file for the set of packages to be (re) build,
for example:

```
# Recipe for python collections
---
python33:
  - name: Python 3.3
  - packages:
    - python33
    - python
    - python-setuptools
    - python-docutils
    - python-markupsafe
    - python-jinja2
      - with_docs 0
    - python-coverage
    - python-nose
      - with_docs 0
    - python-sphinx
    - python-pygments
    - python-jinja2
    - python-nose
    - python-simplejson
    - python-virtualenv
    - python-sqlalchemy
```

The first phase is to generate the scenario script, based on recipe for
particular collection and a plan for partucular use case. The scenario
script will be run by user afterwards.

Several examples how the script may be generated:

```
rebuild mock python33.yml >python33-mock.sh
rebuild rhpkg python33.yml >python33-rhpkg.sh
rebuild centpkg python33.yml --pkgnum=3 >python33-centpkg.sh
rebuild copr --srpm-ssh=fedorepeople.org:public_html/colname \
             --srpm-wget=myname.fedorapeople.org/colname python33.yml \
             >python33-copr.sh
```

The second phase is the running the scenario script itself:

```
./python33-mock.sh
./python33-rhpkg.sh --help
./python33-rhpkg.sh --commit
./python33-rhpkg.sh 
./python33-rhpkg.sh --startpkg=python33-python-sphinx
./python33-rhpkg.sh --steps=3
```

How to write a plan
-------------------
A plan is a set of shell scriptlets that are sourced in the generated
shell recipy.

We have the following scriptlets that are sourced in the following order
if the script is available:

* init
* prepare
* adjust
* store
* build

The `init` section is run once in the begining of the session, the rest
of scriptlets are run once per every package.

Section `prepare` usually unpack sources and changes working directory into
the directory that holds the SPEC file.

Section `adjust` may be used for any specific changes, like adjusting `Release`
in the SPEC file.

Between `adjust` and `store` the necessary tasks are done, based on the recipe.

Section `store` may be used for committing changes in the spec back to its
source.

Section `build` is then usually used for running the build and waiting for
result if needed.


How to write a plan specification:
----------------------------------

Plan specification is very simple set of key/values pairs so we can produce
more similar scenarios with only specific values changed without need to have
duplicit code in the plan scripts. Generally every value in the plan
specification is exported in the plan scripts, while the plan scripts are
then evaluated using jinja templating engine.

```
---
name: Plan to rebuild SCL in mock
dir: plans/mock
mock: rhel-6-core
reference_bug: #123456
local_dir: /home/myuser/rebuild_scl01
prefix_packages: scl01-
```
