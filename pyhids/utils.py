import pickle
from contextlib import contextmanager
from typing import Dict

from cuckoo.filter import CuckooFilter  # type: ignore
from flor import BloomFilter  # type: ignore

import conf


@contextmanager
def opened_w_error(filename: str, mode: str = "r"):
    try:
        f = open(filename, mode)
    except OSError as err:
        yield None, err
    else:
        try:
            yield f, None
        finally:
            f.close()


def load_base() -> Dict[str, Dict[str, str]]:
    """Load the database.

    Return a dictionnary wich contains filenames and theirs hash value.
    """
    database = None
    with opened_w_error(conf.DATABASE, "rb") as (serialized_database, err):
        if err or serialized_database is None:
            print(str(err))
            exit(1)
        else:
            database = pickle.load(serialized_database)
    return database


def bloom_export():
    """Generates a Bloom filter with all the data from the database
    of pyHIDS. The result is written on the disk and returned as a
    BloomFilter object.
    """
    base = load_base()
    bf = BloomFilter(n=conf.BLOOM_CAPACITY, p=conf.BLOOM_FALSE_POSITIVE_PROBABILITY)
    for sha1 in base["files"].values():
        bf.add(sha1.upper().encode("utf-8"))
    export_location = conf.BLOOM_LOCATION + "bloomfilter.bf"
    with opened_w_error(export_location, "wb") as (f, err):
        if err:
            print(str(err))
            exit(1)
        else:
            bf.write(f)
    print(f"Bloom filter generated and stored: {export_location}")
    return bf


def cuckoo_export():
    """Generates a Cuckoo filter with all the data from the database
    of pyHIDS. The result is written on the disk and returned as a
    CuckooFilter object.
    """
    base = load_base()
    cuckoo = CuckooFilter(
        capacity=conf.CUCKOO_CAPACITY, error_rate=conf.CUCKOO_ERROR_RATE
    )
    for sha1 in base["files"].values():
        cuckoo.insert(sha1.upper().encode("utf-8"))
    export_location = conf.CUCKOO_LOCATION + "cuckoofilter.cf"
    serialized_cuckoo = open(export_location, "wb")
    pickle.dump(cuckoo, serialized_cuckoo)
    serialized_cuckoo.close()
    print(f"Cuckoo filter generated and stored: {export_location}")
    return cuckoo
