#! /usr/bin/env python

from typing import Any, Dict, Optional, Tuple

import pyhashlookup

import conf
from pyhids import utils


def check_result(result: Dict[str, Any]) -> Tuple[Optional[bool], Dict]:
    if "message" in result:
        # Unknown in db
        return None, {}

    legit = None
    details = {}
    if "KnownMalicious" in result:
        legit = False
        details["malicious"] = result["KnownMalicious"]

    if "hashlookup:trust" in result:
        if "source" in result:
            details["source"] = result["source"]
        if "FileName" in result:
            details["filename"] = result["FileName"]
        if result["hashlookup:trust"] < 50:
            legit = False
        elif legit is not False:
            legit = True
    return legit, details


def main():
    base = utils.load_base()
    pylookup = pyhashlookup.Hashlookup(root_url=conf.HASHLOOKUP_URL)
    hashes = list(base["files"].values())
    # hashes.append("C18E2AACF02FACBCAD29D20593E823A1C7A088E98AB3A06E48E46821B63A1BF5")
    result = pylookup.lookup(hashes)
    malicious_files = {}
    for elem in result:
        sha1_legit, sha1_details = check_result(elem)
        if None is not sha1_legit:
            malicious_files[sha1_legit] = sha1_details
    print(malicious_files)


if __name__ == "__main__":
    main()
