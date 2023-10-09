import pickle

from cuckoo.filter import CuckooFilter
from flor import BloomFilter

import conf


def load_base():
    """Load the database.

    Return a dictionnary wich contains filenames and theirs hash value.
    """
    database = None
    with open(conf.DATABASE, "rb") as serialized_database:
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
    with open(conf.BLOOM_LOCATION, "wb") as f:
        bf.write(f)
    print(f"Bloom filter generated and stored: {conf.BLOOM_LOCATION}")
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
    serialized_cuckoo = open(conf.CUCKOO_LOCATION, "wb")
    pickle.dump(cuckoo, serialized_cuckoo)
    serialized_cuckoo.close()
    print(f"Cuckoo filter generated and stored: {conf.CUCKOO_LOCATION}")
    return cuckoo
