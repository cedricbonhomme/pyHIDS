#! /usr/bin/env python

import pyhashlookup

import conf
from pyhids import utils

base = utils.load_base()


pylookup = pyhashlookup.Hashlookup(root_url=conf.HASHLOOKUP_URL)

result = pylookup.lookup(list(base["files"].values()))

print(result)
