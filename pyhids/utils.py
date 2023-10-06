import pickle

import conf


def load_base():
    """Load the database.

    Return a dictionnary wich contains filenames and theirs hash value.
    """
    database = None
    with open(conf.DATABASE, "rb") as serialized_database:
        database = pickle.load(serialized_database)
    return database
