import argparse
import pathlib
from importlib.metadata import metadata
from logging import INFO, StreamHandler, getLogger

import pypdf

_package_metadata = metadata(__package__)
__version__ = _package_metadata["Version"]
__author__ = _package_metadata.get("Author-email", "")
logger = getLogger(__name__)
logger.addHandler(StreamHandler())
logger.setLevel(INFO)


def mergepdf(input_dir, output_file, sorted_key):
    """Merge PDF files."""
    lst = sorted(map(str, pathlib.Path(input_dir).rglob("*.pdf")))
    key = eval(f"lambda s: f'{sorted_key}'") if sorted_key else None
    if key:
        lst = sorted(lst, key=key)
        logger.info(lst)
    merger = pypdf.PdfWriter()
    merger.strict = False
    try:
        logger.info("Including")
        for file in lst:
            merger.append(file, import_outline=False)
            logger.info(" %s%s", file, (" as " + key(file)) if key else "")
        merger.write(output_file)
    finally:
        merger.close()
        logger.info("Output %s", output_file)


def main():
    parser = argparse.ArgumentParser(description=mergepdf.__doc__)
    parser.add_argument("-i", "--input-dir", default=".")
    parser.add_argument("-o", "--output-file", default="out.pdf")
    parser.add_argument("-k", "--sorted-key")
    args = parser.parse_args()
    mergepdf(args.input_dir, args.output_file, args.sorted_key)
