#!/usr/bin/env python

import argparse

from pyhids.genKeys import main as genKeys
from pyhids.genBase import main as genBase
from pyhids.pyHIDS import main as run


def main():
    parser = argparse.ArgumentParser(prog="pyhids")
    subparsers = parser.add_subparsers(
        help="sub-command help", dest="command", required=True
    )

    # Subparser: gen-keys
    parser_gen_keys = subparsers.add_parser("gen-keys", help="gen-keys help")
    parser_gen_keys.add_argument(
        "-s",
        "--size",
        dest="nb_bits",
        default=2048,
        required=True,
        type=int,
        help="The number of bits for the RSA keys.",
    )

    # Subparser: gen-base
    parser_gen_base = subparsers.add_parser("gen-base", help="gen-base help")
    parser_gen_base.add_argument(
        "--sign",
        dest="sign_database",
        default=False,
        action=argparse.BooleanOptionalAction,
        help="Specify if the database must be signed. ",
    )

    # Subparser: run
    parser_run = subparsers.add_parser("run", help="run help")
    parser_run.add_argument(
        "--check-signature",
        dest="check_signature",
        default=False,
        action=argparse.BooleanOptionalAction,
        help="Specify if the signature of the database must be checked. ",
    )

    arguments = parser.parse_args()

    if arguments.command == "gen-keys":
        genKeys(arguments.nb_bits)
    elif arguments.command == "gen-base":
        genBase(arguments.sign_database)
    elif arguments.command == "run":
        run(arguments.check_signature)
    else:
        return "Unknown sub-command."


if __name__ == "__main__":
    # Point of entry in execution mode
    main()
