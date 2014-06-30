#!/usr/bin/env python

# Wrapper to demo basic functionality
# clean up the code, abstract out common areas and add cmdline switches

import sys
import os
import importlib

def get_usage(provider):
    # get list of valid_providers
    valid_providers = []
    base_dir = os.path.join(os.path.dirname(__file__), 'providers')
    for fname in os.listdir(base_dir):
        full_path = os.path.join(base_dir, fname)
        if os.path.isdir(full_path):
            valid_providers.append(fname)

    # validate input
    if len(valid_providers) == 0:
        raise ValueError('No internet valid_providers added')

    if provider not in valid_providers:
        raise ValueError('Invalid provider - %s. Valid providers - %s' % (provider, valid_providers))

    # import provider
    provider_mod = importlib.import_module('netchecker.providers.%s.main' % provider)

    # get provider usage
    obj = provider_mod.NetProvider()
    return obj.usage

def main(argv):
    if len(argv) != 2:
        raise ValueError('Usage: %s %s' % (argv[0], 'provider'))
    return get_usage(argv[1])

if __name__ == '__main__':
    print main(sys.argv)
