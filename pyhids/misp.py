#! /usr/bin/env python

from pymisp import PyMISP

import conf
from pyhids import utils

misp_url = conf.MISP_URL
misp_key = conf.MISP_KEY
misp_verifycert = True
relative_path = "attributes/restSearch"
body = {
    # "org": "CIRCL",
    "returnFormat": "json",
    "type": "filename|sha1",
}


def main():
    misp = PyMISP(misp_url, misp_key, misp_verifycert)
    alerts = []
    base = utils.load_base()
    for _path, sha1 in list(base["files"].items()):
        # filename = os.path.basename(_path)
        body["value"] = sha1
        result = misp.direct_call(relative_path, body)
        if result["Attribute"]:
            alerts.append(result)
    if alerts:
        print(alerts)


if __name__ == "__main__":
    main()
