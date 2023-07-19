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
    
    # Subparser: gen-base
    parser_gen_base = subparsers.add_parser("gen-base", help="gen-base help")

    # Subparser: run
    parser_run = subparsers.add_parser("run", help="run help")

    arguments = parser.parse_args()

    if arguments.command == "gen-keys":
        genKeys()
    elif arguments.command == "gen-base":
        genBase()
    elif arguments.command == "run":
        run()
    else:
        return "Unknown sub-command."


if __name__ == "__main__":
    # Point of entry in execution mode
    main()