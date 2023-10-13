#! /usr/bin/env python

"""Uses Yara in order to verify the files.
"""

import glob
import pprint

import yara  # type: ignore

import conf
from pyhids import utils


def main():
    pp = pprint.PrettyPrinter(indent=4)
    try:
        yara_file = glob.glob(conf.YARA_RULES + "*.yara")[0]
        rules = yara.compile(yara_file)
    except Exception as e:
        raise Exception("Problem when compiling the YARA rules.") from e
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
