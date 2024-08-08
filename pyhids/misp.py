#! /usr/bin/env python

"""Query a MISP server in order to verify the hashes of the files.
"""

import logging

from pymisp import PyMISP

import conf
from pyhids import utils

logging.getLogger("pymisp").setLevel(logging.CRITICAL)

misp_url = conf.MISP_URL
misp_key = conf.MISP_KEY
misp_verifycert = True
relative_path = "attributes/restSearch"
# body = {
#     # "org": "CIRCL",
#     "returnFormat": "json",
#     "type": "filename|sha1",
# }
values = {}


def main(return_format: str = "json", pythonify: bool = False) -> None:
    try:
        misp = PyMISP(misp_url, misp_key, misp_verifycert)
    except Exception as e:
        print("Unable to instantiate PyMISP object:")
        print(str(e))
        exit(1)
    # alerts = []
    base = utils.load_base()
    i = 0
    for _path, sha1 in list(base["files"].items()):
        i += 1
        # filename = os.path.basename(_path)
        values[f"value{i}"] = sha1
    result = misp.search(
        controller="attributes",
        value=values,
        pythonify=pythonify,
        return_format=return_format,
    )
    if result:
        print(result)


if __name__ == "__main__":
    main()
