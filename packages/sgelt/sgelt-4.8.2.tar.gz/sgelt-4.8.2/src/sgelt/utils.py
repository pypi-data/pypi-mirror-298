import filecmp
import unicodedata
import unidecode
import re
from markupsafe import Markup
from datetime import datetime, date
import datetimejson
import shutil
from pathlib import Path
import logging
import markdown
from markdown_link_attr_modifier import LinkAttrModifierExtension
import frontmatter
import random
import socket
import sys
import yaml

from .mdextend import TableExtension

log = logging.getLogger(__name__)

REG_SUB = (
    (r"""\/|"|'""", '-'),  # replace /, " and ' by -
    (r"\||\?|\,", ''),  # remove |, ? and ,
    (r'(?u)\A\s*', ''),  # strip leading whitespace
    (r'(?u)\s*\Z', ''),  # strip trailing whitespace
    (r'[-\s]+', '-'),  # reduce multiple whitespace or '-' to single '-'
)

md = markdown.Markdown(extensions=[
    'toc', 'attr_list', 'tables',
    LinkAttrModifierExtension(new_tab='external_only',
                              no_referrer='external_only'),
    TableExtension()])


def slugify(value, regex_subs=REG_SUB):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    Took from Pelican sources.
    """

    def normalize_unicode(text):
        # normalize text by compatibility composition
        # see: https://en.wikipedia.org/wiki/Unicode_equivalence
        return unicodedata.normalize('NFKC', text)

    # strip tags from value
    value = Markup(value).striptags()

    # normalization
    value = normalize_unicode(value)

    # ASCII-fy
    value = unidecode.unidecode(value)

    # perform regex substitutions
    for src, dst in regex_subs:
        value = re.sub(
            normalize_unicode(src),
            normalize_unicode(dst),
            value,
            flags=re.IGNORECASE)

    value = value.lower()

    return value.strip()


def md_slugify(value: str) -> str:
    """slugify string using markdown extension slugifier"""
    return markdown.extensions.toc.slugify(value, '-')


def slugify_path(path: Path) -> Path:
    """Return slugified path"""
    return Path('.').joinpath(*(slugify(p) for p in path.parts))


def copy_file(src: Path, dest: Path):
    """Copy src file to dest file if files are different"""

    def do_copy(src, dest):
        """Log and copy"""
        log.debug(f'Copy {src} to {dest}')
        shutil.copyfile(src, dest)

    # Create parent directory if not exists
    dest.parent.mkdir(exist_ok=True, parents=True)
    try:
        if dest.is_file():
            # if destination file exists,
            if not filecmp.cmp(src, dest):
                # copy only if files are different
                do_copy(src, dest)
            else:
                log.debug(f"files are identical in {src} and {dest}")
        else:
            do_copy(src, dest)
    except FileNotFoundError:
        log.error(f'Attachment file "{src}" not found')


def read_data(json_path: Path) -> dict:
    """Read json file and return dict"""
    with open(json_path) as json_file:
        return datetimejson.load(json_file)


class MetaDataParsingError(Exception):
    """A class to handle Markdown files parsing errors"""

    def __init__(self, md_filepath, metadata,
                 message="Error parsing file metadata"):
        self.md_filepath = md_filepath
        self.metadata = metadata
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return (f"""\
{self.message} for {self.md_filepath}: date field \
{self.metadata['date']} is not formed as datetime or date. \
"See https://jekyllrb.com/docs/front-matter/#predefined-variables-for-posts"
""")


def parse_md_file(md_filepath: Path) -> tuple:
    """
    Parse markdown file to return a tuple of metadata and markdown content
    """
    file_content = md_filepath.read_text()
    try:
        metadata, md_content = frontmatter.parse(file_content)
        try:
            try:
                if type(metadata['date']) not in (datetime, date):
                    raise MetaDataParsingError(
                        md_filepath=md_filepath, metadata=metadata)
            except MetaDataParsingError as e:
                log.error(e)
                sys.exit(1)
        except KeyError:
            pass
        return metadata, md_content

    except (yaml.scanner.ScannerError, yaml.parser.ParserError) as e:
        log.error(f"Cannot parse {md_filepath}:\n{file_content}\nReason: {e}")
        sys.exit(1)


def clean_project(output_path: Path):
    """Clean project"""
    try:
        shutil.rmtree(output_path)
        log.info(f"Deleted directory: '{output_path}'")
    except FileNotFoundError as e:
        log.warning(f"Cleaning project: '{e.filename}' does not exist")


def override_default(paths: list, dcmp):
    """
    Populate the paths list with files from left and right dcmp object.
    Use right file if presents.
    """

    def extend_with_path_content(basepath: str, names: list):
        """Add all files from names list to paths list"""
        for name in names:
            path = Path(basepath) / name
            if path.is_file():
                paths.append(path)
            else:
                paths.extend(path.glob('**/*'))

    # Add files that are only in left dir
    extend_with_path_content(dcmp.left, dcmp.left_only)
    # Add files that are only in right dir
    extend_with_path_content(dcmp.right, dcmp.right_only)

    # For common files add right version
    for name in dcmp.common_files:
        paths.append(Path(dcmp.right) / name)

    # Recursive call to subdirectories
    for sub_dcmp in dcmp.subdirs.values():
        override_default(paths, sub_dcmp)


def get_socket_port() -> int:
    """Return 5500 or an arbitrary unused port"""
    s = socket.socket()
    try:
        # Try default port 5500
        s.bind(('', 5500))
    except OSError:
        log.info('Port 5500 is in use, trying an arbitrary port')
        s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()
    return port


def get_short_uid() -> int:
    """Return a unique 6-digit string"""
    return random.randint(100000, 999999)
