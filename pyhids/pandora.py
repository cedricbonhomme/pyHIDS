#! /usr/bin/env python

"""Query a Pandora server in order to verify the hashes of the files.
"""

import pypandora

import conf
from pyhids import utils


def main() -> None:
    base = utils.load_base()
    pandora = pypandora.PyPandora(root_url=conf.PANDORA_URL)
    api_key = pandora.get_apikey(conf.PANDORA_USERNAME, conf.PANDORA_PASSWORD)
    try:
        pandora.init_apikey(
            conf.PANDORA_USERNAME, conf.PANDORA_PASSWORD, api_key["authkey"]
        )
    except Exception as e:
        print("Unable to initialize the API key:")
        print(e)
        exit(1)
    alerts, hashes = [], list(base["files"].values())
    for hash_value in hashes:
        result = pandora.search(hash_value)
        if "matching_tasks" in result and result["matching_tasks"]:
            for elem in result["matching_tasks"]:
                task_status = pandora.task_status(elem)
                task_status["file_hash"] = hash_value
                alerts.append(task_status)
    if alerts:
        print(alerts)


if __name__ == "__main__":
    main()
