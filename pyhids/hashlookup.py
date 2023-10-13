#! /usr/bin/env python

"""Query a Hashlookup server in order to verify the hashes of the files.
"""

from typing import Any, Dict, Optional, Tuple

import pyhashlookup

import conf
from pyhids import utils


def check_result(result: Dict[str, Any]) -> Tuple[Optional[bool], Dict]:
    """Checks the result returned from a Hashlookup server."""
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
    pylookup = pyhashlookup.Hashlookup(root_url=conf.HASHLOOKUP_URL)
    base = utils.load_base()
    hashes = list(base["files"].values())
    result = pylookup.lookup(hashes)
    malicious_files = {}
    for elem in result:
        sha1_legit, sha1_details = check_result(elem)
        if None is not sha1_legit:
            malicious_files[elem["SHA-1"]] = sha1_details
    for sha, details in malicious_files.items():
        print("{} {}".format(sha, " ".join([f"{k}:{v}" for k, v in details.items()])))


if __name__ == "__main__":
    main()
