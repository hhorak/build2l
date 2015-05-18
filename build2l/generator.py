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

def main():

    parser = argparse.ArgumentParser(description='Tool to build or rebuild packages.',
                                 epilog="This is an open-source project by Red Hat.")
    parser.add_argument('--version', action='version', version='%(prog)s {}'.format(PROGRAM_VERSION))
    parser.add_argument('--recipe', metavar='file', required=True,
                        help='Recipe file that describes packages set')
    parser.add_argument('--plan', metavar='file', required=True,
                        help='Plan file that describes what to do with packages')
    parser.add_argument('--collection', metavar='id', required=True,
                        help='ID if collection from recipe')
    args = parser.parse_args()
    plan = yaml.load(open(os.path.join(PLANS_DIR, args.plan + '.yml'), 'r'))
    print('#!/bin/bash')
    print('if [ $# -ne {0} ] ; then echo "Usage: `basename $0` {1}" ; exit 1 ; fi'.format(str(len(plan['values'])), " ".join(plan['values'].keys())))
    for k in plan['values']:
        print(k + '={$1:-' + str(plan['values'][k]) + '} ; shift')
    recipe = yaml.load(open(args.recipe, 'r'))
    for package in recipe[args.collection]['packages']:
        handle_script(args.plan, EVENT_PRE, package, plan['values'])
        print ("# here we do some SPEC adjustments")
        handle_script(args.plan, EVENT_POST, package, plan['values'])

if __name__ == '__main__':
    exit(main())

