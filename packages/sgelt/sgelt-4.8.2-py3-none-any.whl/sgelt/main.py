"""Build a static website"""

import argparse
import locale
import logging
import sys
from pathlib import Path


from . import sgelt, utils, config, watch, serve, __version__

log = logging.getLogger(__name__)
try:
    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
except locale.Error:
    log.warning("Could not set locale to fr_FR.UTF-8")


def parse_args(args: list) -> argparse.Namespace:
    """Parse list of arguments and return an Namespace"""
    formatter = argparse.RawDescriptionHelpFormatter
    parser = argparse.ArgumentParser(description=globals()['__doc__'],
                                     formatter_class=formatter)
    parser.add_argument('-d', '--debug', action='store_true',
                        help="Activate bug verbosity level")
    parser.add_argument('-cf', '--config', type=str,
                        help="Specify YAML config filename",
                        default=Path(config.Config.def_conf['config_path']))
    parser.add_argument('-ja', '--json_agenda', type=str,
                        help="Specify json agenda filename")
    parser.add_argument('-jt', '--json_teams', type=str,
                        help="Specify json teams filename")
    parser.add_argument('-c', '--content', type=str,
                        help="Specify content directory path")
    parser.add_argument('-o', '--output', type=str,
                        help="Specify output directory path")
    parser.add_argument('-ni', '--noindex', dest='search_index',
                        action='store_false', default=True,
                        help="Do not build search index")
    watcher = parser.add_argument_group(
        'watch', description="Watch for content/")
    watcher.add_argument('-s', '--serve', action="store_true",
                         help="Launch a local web server")
    watcher.add_argument('-b', '--browser', action="store_true",
                         help="Open the URL in a web browser")
    watcher.add_argument('-a', '--auto', action="store_true",
                         help="Build site in auto (watch) mode")
    clean = parser.add_argument_group(
        'clean', description="Clean all files")
    clean.add_argument('-r', '--reset', action='store_true',
                       help="Clean output files")
    version = parser.add_argument_group(
        'version', description="Show version and exit")
    version.add_argument('-v', '--version', action='store_true',
                         help="Show version and exit")
    return parser.parse_args(args)


def main():
    """Entrypoint for sgelt"""

    args = parse_args(sys.argv[1:])

    logging.basicConfig(level=logging.DEBUG
                        if args.debug else logging.INFO)

    if args.browser and not args.serve:
        exit("-b/--browser cannot be used without -s/--serve")

    # Instantiate and load a Config object
    conf = config.Config(args=args)
    conf.load()

    if args.reset:
        utils.clean_project(conf.output_path)
        return

    if args.version:
        print(f"Sgelt {__version__}")
        return

    if args.serve:
        server = serve.MyServer(conf)
        if args.auto:
            # watch for changes to rebuild
            server.watch()
        server.serve(args.browser)
    elif args.auto:
        watch.watch(conf)
    else:
        # Instantiate, build a Website and exit
        website = sgelt.Website(conf)
        website.build()


if __name__ == "__main__":
    main()
