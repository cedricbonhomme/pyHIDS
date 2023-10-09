import pickle

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
    bf = BloomFilter(n=conf.CAPACITY, p=conf.FALSE_POSITIVE_PROBABILITY)
    for sha1 in base["files"].values():
        bf.add(sha1)
    with open(conf.BLOOM_LOCATION, "wb") as f:
        bf.write(f)
    return bf
