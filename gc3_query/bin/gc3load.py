# -*- coding: utf-8 -*-

"""Console script for gc3query."""
import sys

from gc3_query.lib.cli.gc3load import *

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)

if __name__ == "__main__":
    try:
        cli()
    except KeyboardInterrupt:
        print(f"Caught KeyboardInterrupt, shutting down.")
        sys.exit(0)
