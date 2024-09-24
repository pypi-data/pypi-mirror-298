#!/usr/bin/env python3
"""
Command line utility that helps serialize brick models to json
"""
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, SUPPRESS
import agx
from brickbundles import bundle_path
from rebrick import serialize_brick_file, __version__, set_log_level
from rebrick.versionaction import VersionAction


def parse_args():
    parser = ArgumentParser(description="Serialize brick models", formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("brickfile", help="the .brick file to serialize")
    parser.add_argument("--bundle-path", help="list of path to bundle dependencies if any. Overrides environment variable BRICK_BUNDLE_PATH.",
                        metavar="<bundle_path>", default=bundle_path())
    parser.add_argument("--loglevel", choices=["trace", "debug", "info", "warn", "error", "critical", "off"], help="Set log level", default="warn")
    parser.add_argument("--modelname", help="The model to serialize (defaults to last model in file)", metavar="<name>", default="")
    parser.add_argument("--version", help="Show version", action=VersionAction, nargs=0, default=SUPPRESS)
    return parser.parse_args()


def run():
    args = parse_args()
    set_log_level(args.loglevel)

    # Must initialize agx for plugin to work
    _ = agx.init()

    result = serialize_brick_file(args.brickfile, args.bundle_path, args.modelname)
    print(result)


if __name__ == '__main__':
    run()
