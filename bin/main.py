#!/usr/bin/env python

import argparse

from pyhids import get_version, utils
from pyhids.genBase import main as genBase
from pyhids.genKeys import main as genKeys
from pyhids.hashlookup import main as hashlookup
from pyhids.misp import main as misp
from pyhids.pandora import main as pandora
from pyhids.pyHIDS import main as run
from pyhids.yara_ext import main as yara


def main():
    parser = argparse.ArgumentParser(prog="pyhids")
    subparsers = parser.add_subparsers(
        help="sub-command help", dest="command", required=False
    )

    parser.add_argument(
        "--version",
        action="store_true",
        help="Display the version of pyHIDS.",
    )

    # Subparser: gen-keys
    parser_gen_keys = subparsers.add_parser(
        "gen-keys", help="Generates RSA keys in order to verify the database of hashes."
    )
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
    parser_gen_base = subparsers.add_parser(
        "gen-base", help="Generates the database of files to monitor."
    )
    parser_gen_base.add_argument(
        "--sign",
        action="store_true",
        help="Specify if the database must be signed.",
    )

    # Subparser: run
    parser_run = subparsers.add_parser(
        "run", help="Executes pyHIDS in order to verify the integrity of the files."
    )
    parser_run.add_argument(
        "--check-signature",
        action="store_true",
        help="Specify if the signature of the database must be checked.",
    )
    parser_run.add_argument(
        "--verbose",
        action="store_true",
        help="Specify if the output must be verbose.",
    )

    # Subparser: hashlookup
    subparsers.add_parser(
        "hashlookup", help="Uses Hashlookup in order to verify the hashes of the files."
    )

    # Subparser: pandora
    subparsers.add_parser(
        "pandora", help="Uses Pandora in order to verify the hashes of the files."
    )

    # Subparser: MISP
    parser_misp = subparsers.add_parser(
        "misp", help="Uses MISP in order to verify the hashes of the files."
    )
    parser_misp.add_argument(
        "--pythonify",
        action="store_true",
        help="Returns a list of PyMISP Objects instead of the plain json output.",
    )
    parser_misp.add_argument(
        "--return-format",
        choices=[
            "openioc",
            "json",
            "xml",
            "suricata",
            "snort",
            "text",
            "rpz",
            "csv",
            "cache",
            "stix-xml",
            "stix",
            "stix2",
            "yara",
            "yara-json",
            "attack",
            "attack-sightings",
            "context",
            "context-markdown",
        ],
        default="json",
        help="Set the return format of the search.",
    )

    # Subparser: Yara
    subparsers.add_parser("yara", help="Uses Yara in order to verify the files.")

    # Subparser: Export
    parser_export = subparsers.add_parser("export", help="Provide export functions.")
    parser_export.add_argument(
        "--bloom-filter",
        action="store_true",
        help="Export the database in a Bloom filter.",
    )
    parser_export.add_argument(
        "--cuckoo-filter",
        action="store_true",
        help="Export the database in a Cuckoo filter.",
    )

    arguments = parser.parse_args()

    if arguments.version:
        return get_version()

    if arguments.command == "gen-keys":
        genKeys(arguments.nb_bits)
    elif arguments.command == "gen-base":
        genBase(arguments.sign)
    elif arguments.command == "run":
        run(arguments.check_signature, arguments.verbose)
    elif arguments.command == "hashlookup":
        hashlookup()
    elif arguments.command == "pandora":
        pandora()
    elif arguments.command == "misp":
        misp(return_format=arguments.return_format, pythonify=arguments.pythonify)
    elif arguments.command == "yara":
        yara()
    elif arguments.command == "export":
        if arguments.bloom_filter:
            utils.bloom_export()
        elif arguments.cuckoo_filter:
            utils.cuckoo_export()
        else:
            return "Unknown export format."
    else:
        return "Unknown arguments or options.\nFor help type:\n\tpyhids --help"


if __name__ == "__main__":
    # Point of entry in execution mode
    main()
