"""SGELT: a (static) Site GEnerator for Labs and Teams"""

import filecmp
import itertools
import json
import logging
import shutil
import time

from .data import Data
from .pages import (ConferencePage, DefensePage, HomePage, IndexPage,
                    LibNewsIndexPage, LibNewsPage, MdPage, NewsIndexPage,
                    NewsPage, Page, SeminarPage, SeminarTopIndexPage,
                    WorkGroupTopIndexPage, VirtualNewsPage)
from .utils import copy_file, override_default, parse_md_file

log = logging.getLogger(__name__)


class Website:

    def __init__(self, conf):
        self.conf = conf
        # Load agenda and team data from json files
        self.data = Data(self.conf)
        self.data.read_files()
        self.pages = None
        self.index_nodes = []  # a list of search index nodes

    def _get_menu_item(self, prefix: str) -> str:
        """Search fo prefix in config.yml: nav_items"""
        for item_name, sub_items in self.conf.site['nav_items'].items():
            try:
                for url in sub_items.values():
                    if url.startswith(prefix):
                        return item_name
            except AttributeError:
                pass
        return None

    def html_pages(self):
        """Return a generator for raw html pages"""

        def is_a_static_page(s):
            """Return True if s targets a static Page"""
            try:
                return not (s.startswith('https://')
                            or s.startswith('http://')
                            or s == '#')
            except AttributeError:
                # s is not a string
                return False

        # Create a static pages if relevant
        for menu_item, v in self.conf.site['nav_items'].items():
            if is_a_static_page(v):
                yield Page(self, v, menu_item)

    def conf_pages(self):
        """Return a generator for conference pages"""

        for conference in self.data.conferences:
            yield ConferencePage(self,
                                 menu_item="Agenda",
                                 title=conference['title'],
                                 template_name="conference.html",
                                 category='conférence',
                                 event=conference)

    def def_pages(self):
        """Return a generator for defense pages"""

        for defense in self.data.defenses:
            yield DefensePage(self,
                              menu_item="Agenda",
                              title=defense['title'],
                              template_name="soutenance.html",
                              category='soutenance',
                              event=defense)

    def sem_pages(self):
        """Return a generator for seminar pages"""

        for seminar in self.data.seminars:
            seminarpage = SeminarPage(self,
                                      menu_item="Agenda",
                                      title=seminar['title'],
                                      template_name="seminaire.html",
                                      category=seminar['type'].lower(),
                                      seminar=seminar,
                                      events=seminar['events'])
            yield seminarpage

    def seminars_index(self):
        """Return a generator for seminar index page"""

        for status in 'actif', 'passé':
            yield SeminarTopIndexPage(
                self,
                menu_item='Agenda',
                title='Séminaires',
                template_name="seminaires.html",
                seminars=self.data.seminars,
                status=status)

    def workgroups_index(self):
        """Return a generator for seminar index page"""

        for status in 'actif', 'passé':
            yield WorkGroupTopIndexPage(
                self,
                menu_item='Agenda',
                title='Groupes de travail',
                template_name="seminaires.html",
                seminars=self.data.seminars,
                status=status)

    def agenda_index(self):
        """Return a generator for conferences and full agenda pages"""

        # Conférence agenda
        yield IndexPage(self,
                        menu_item='Agenda',
                        title='Conférences et rencontres',
                        template_name='agenda.html',
                        filename='index.html',
                        category='conférence',
                        events=self.data.conferences)

        # Soutenance agenda
        yield IndexPage(self,
                        menu_item='Agenda',
                        title='Soutenances',
                        template_name='agenda.html',
                        filename='index.html',
                        category='soutenance',
                        events=self.data.defenses)

        # À venir (all categories)
        coming_events = [event for event in self.data.events
                         if event['date'].date() >= self.conf.site['today']]
        yield IndexPage(self,
                        menu_item='Agenda',
                        title='À venir',
                        template_name='agenda.html',
                        filename='a_venir.html',
                        events=coming_events)

    def md_pages(self):
        """Return a generator for markdown pages"""

        # Loop on markdown files from content/ dir
        # excluding directories starting with .
        md_filepaths = (
            md_filepath for md_filepath
            in self.conf.content_path.glob('**/*.md')
            if not md_filepath.parent.name.startswith('.'))
        for md_filepath in md_filepaths:
            # Read metadata and content
            metadata, md_content = parse_md_file(md_filepath)
            category = metadata.get('category')
            if category == 'news':
                if metadata.get('external_url'):
                    yield VirtualNewsPage(self,
                                          md_filepath, metadata,
                                          md_content,
                                          template_name="article.html")
                else:
                    yield NewsPage(self, md_filepath, metadata, md_content,
                                   template_name="article.html")
            if category == 'libnews':
                yield LibNewsPage(self,
                                  md_filepath, metadata,
                                  md_content)
            elif category == 'homecard':
                # implemented later in homepage()
                pass
            else:
                template_name = ('equipe.html' if category == 'team'
                                 else 'article.html')
                yield MdPage(self, md_filepath, metadata, md_content,
                             template_name=template_name)

    def news_index(self):
        """Return a generator for news page"""
        yield NewsIndexPage(self)

    def libnews_index(self):
        """Return a generator for news page"""
        menu_item = self._get_menu_item('libnews')
        yield LibNewsIndexPage(self, menu_item=menu_item)

    def homepage(self):
        """Return a generator for homepage"""
        yield HomePage(self, title=self.conf.site['homepage']['title'])

    def get_article_pages(self):
        """Get pages generators from data"""
        pages = itertools.chain(self.conf_pages(),
                                self.def_pages(),
                                self.sem_pages(),
                                self.md_pages(),
                                self.html_pages())
        return pages

    def get_index_pages(self):
        """Get pages generators from data"""
        pages = itertools.chain(self.seminars_index(),
                                self.workgroups_index(),
                                self.agenda_index(),
                                self.news_index(),
                                self.libnews_index(),
                                self.homepage())
        return pages

    def get_all_pages(self):
        """Get pages generators from data"""
        pages = itertools.chain(self.get_article_pages(),
                                self.get_index_pages())
        return pages

    def copy_attachments(self,):
        """Copy attachments files from content_path/ to output_path/"""
        # Create a path generator for all files except .md
        attachments = (path for path in self.conf.content_path.glob('**/*')
                       if path.is_file() and path.suffix != '.md' and
                       not path.parent.name.startswith('.'))
        for src in attachments:
            dst = self.conf.output_path / src.relative_to(
                self.conf.content_path)
            copy_file(src, dst)

    def lunr(self):
        """Write lunr javascript file"""

        root_node = {"pages": self.index_nodes}
        json_dump = json.dumps(root_node, separators=(",", ":"),
                               ensure_ascii=False)
        root_node_js = f"var lunr_index = {json_dump};"

        with open(self.conf.output_path / "lunr_content.js", "w") as f:
            f.write(root_node_js)

    def add_index_node(self, page):
        """If not empty, add a node for lunr.js index json file"""

        index_node = page.get_index_node()
        if isinstance(index_node, dict):
            # append a single node
            self.index_nodes.append(index_node)
        elif isinstance(index_node, list):
            # add a list of nodes from seminar paginated pages
            self.index_nodes += index_node

    def build_pages(self):
        """
        Build site pages and search index.
        """
        log.info("Starting pages generation...")
        start = time.perf_counter()
        self.pages = self.get_all_pages()
        counter = 0
        for page in self.pages:
            page.render()
            if self.conf.search_index:
                # Add node to search index
                self.add_index_node(page)
            counter += page.rendered
        if self.conf.search_index:
            self.lunr()  # build search index
        end = time.perf_counter()
        log.info(f"{counter} pages generated in {end - start:.2f}s")

    def copy_payload(self):
        """Copy payload to output dir"""

        # First build list of payload paths
        static_payload_paths = []
        if not self.conf.theme_path:
            # Use default static path only
            for dirpath in self.conf.static_payload:
                static_payload_paths.extend(
                    (self.conf.default_theme_path / dirpath).glob('**/*'))
        else:
            # Override default static paths with user files
            dcmp = filecmp.dircmp(self.conf.default_theme_path,
                                  self.conf.theme_path,
                                  ignore=['templates'])
            override_default(static_payload_paths, dcmp)

        for path in static_payload_paths:
            # Get relative path
            try:
                relpath = path.relative_to(
                    self.conf.default_theme_path)
            except ValueError:
                relpath = path.relative_to(
                    self.conf.theme_path)

            dst_path = self.conf.output_path / relpath

            log.debug(f"Copying {static_payload_paths} to {dst_path}/")
            dst_path.parent.mkdir(exist_ok=True, parents=True)
            shutil.copyfile(path, dst_path)

    def build(self, clean_output=True):
        """Build website in output_path"""
        output_path = self.conf.output_path
        log.info(f"Building website in {output_path}/ dir")

        # Clean output dir
        if clean_output and output_path.exists():
            shutil.rmtree(output_path)
        output_path.mkdir(exist_ok=True)

        # Copy payload to output dir
        self.copy_payload()

        # Copy attachments files to output dir
        self.copy_attachments()

        # Build site pages and search index
        self.build_pages()


def copy_and_build(conf):
    """Instantiate website, copy attachments and build pages"""
    website = Website(conf)
    website.copy_attachments()
    website.build_pages()
