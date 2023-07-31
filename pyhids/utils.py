import pickle

import conf


def load_base():
    """
    Load the base file.

    Return a dictionnary wich contains filenames
    and theirs hash value.
    """
    # try to open the saved base of hash values
    database = None
    with open(conf.DATABASE, "rb") as serialized_database:
        database = pickle.load(serialized_database)
    # try:
    # base_file = open(conf.DATABASE, "r")
    # except:
    # globals()['warning'] = globals()['warning'] + 1
    # log("Base file " + conf.DATABASE + " does no exist.")
    return database
