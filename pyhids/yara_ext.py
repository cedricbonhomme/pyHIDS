#! /usr/bin/env python

import pprint

import yara

import conf
from pyhids import utils


def main():
    pp = pprint.PrettyPrinter(indent=4)
    try:
        rules = yara.compile(conf.YARA_RULES)
    except Exception as e:
        print("Problem when compiling the YARA rules.")
        print(e)
        exit(1)
    result = {}
    base = utils.load_base()
    for path, _sha1 in list(base["files"].items()):
        try:
            matches = rules.match(path, timeout=60)
        except Exception:
            continue
        if matches:
            result[path] = matches
    if result:
        pp.pprint(result)


if __name__ == "__main__":
    main()
