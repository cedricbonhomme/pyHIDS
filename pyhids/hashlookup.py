#! /usr/bin/env python

import pyhashlookup

import conf
from pyhids import utils


def main():
    base = utils.load_base()
    pylookup = pyhashlookup.Hashlookup(root_url=conf.HASHLOOKUP_URL)
    result = pylookup.lookup(list(base["files"].values()))
    for elem in result:
        print(elem)


if __name__ == "__main__":
    main()
