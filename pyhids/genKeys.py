#! /usr/bin/env python

import pickle

import rsa

import conf


def main(nb_bits: int = 1024):
    print("Generating", nb_bits, "bits RSA keys ...")
    pub, priv = rsa.newkeys(nb_bits)

    public_key = open(conf.PUBLIC_KEY, "wb")
    private_key = open(conf.PRIVATE_KEY, "wb")

    print("Dumping Keys")
    pickle.dump(pub, public_key)
    pickle.dump(priv, private_key)

    public_key.close()
    public_key.close()

    print("Done.")


if __name__ == "__main__":
    main()
