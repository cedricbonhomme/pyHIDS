#! /usr/bin/env python

"""Query a MISP server in order to verify the hashes of the files.
"""

from pymisp import PyMISP

import conf
from pyhids import utils

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


def main(return_format: str = "json", pythonify: bool = False):
    misp = PyMISP(misp_url, misp_key, misp_verifycert)
    # alerts = []
    base = utils.load_base()
    i = 0
    for _path, sha1 in list(base["files"].items()):
        i += 1
        # filename = os.path.basename(_path)
        values[f"value{i}"] = sha1
        # result = misp.direct_call(relative_path, body)
        # if result["Attribute"]:
        #     alerts.append(result)
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
