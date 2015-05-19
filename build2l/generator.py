#!/usr/bin/env python

import argparse
import os
import yaml
from jinja2 import Template

PROGRAM_VERSION=0.1
SCENARIOS_DIR='scenarios'
RECIPES_DIR='recipes'
PLANS_DIR='scripts'
EVENT_PRE='pre'
EVENT_POST='post'

def handle_script(plan, event, package, values):
    values['package'] = package
    with open(os.path.join(PLANS_DIR, event, plan + '.sh'), 'r') as f:
        print(Template(f.read()).render(values))


def get_plan(name, values):
    with open(os.path.join(PLANS_DIR, name + '.yml'), 'r') as f:
        return yaml.load(Template(f.read()).render(values))
    return ''

def main():

    parser = argparse.ArgumentParser(description='Tool to build or rebuild packages.',
                                 epilog="This is an open-source project by Red Hat.")
    parser.add_argument('--version', action='version', version='%(prog)s {}'.format(PROGRAM_VERSION))
    parser.add_argument('--recipe', metavar='file', required=True,
                        help='Recipe file that describes packages set')
    parser.add_argument('--pre', metavar='file', required=True,
                        help='Plan file that describes what to do with packages before adjusting')
    parser.add_argument('--post', metavar='file', required=True,
                        help='Plan file that describes what to do with packages after adjusting')
    parser.add_argument('--collection', metavar='id', required=True,
                        help='ID if collection from recipe')
    args = parser.parse_args()
    plan_pre = get_plan(args.pre, {'collection': args.collection})
    plan_post = get_plan(args.post, {'collection': args.collection})
    print('#!/bin/bash')
    print
    print('set -ex')
    print
    print('source ' + os.path.join(PLANS_DIR, 'lib', 'download_lib.sh'))
    print
    print('if [ "$1" == "-h" ] || [ "$1" == "--help" ] ; then echo "Usage: `basename $0` {0} {1}" ; exit 1 ; fi'.format(" ".join(plan_pre['values'].keys()), " ".join(plan_post['values'].keys())))

    for k in plan_pre['values']:
        print('export ' + k + '=${1:-' + str(plan_pre['values'][k]) + '} ; shift || :')

    for k in plan_post['values']:
        print('export ' + k + '=${1:-' + str(plan_post['values'][k]) + '} ; shift || :')

    recipe = yaml.load(open(args.recipe, 'r'))
    print

    for package in recipe[args.collection]['packages']:
        print('# Rebuild of package {0}'.format(package))

        if '@' in package:
            (package, collection) = package.split('@')
            package=package.strip()+'-'+collection.strip()

        print("pushd $(mktemp -d /tmp/build2l-XXXXXX)")
        handle_script(args.pre, EVENT_PRE, package, plan_pre['values'])
        print ("# here we do some SPEC adjustments")
        handle_script(args.post, EVENT_POST, package, plan_post['values'])
        print("popd")
        print

if __name__ == '__main__':
    exit(main())

