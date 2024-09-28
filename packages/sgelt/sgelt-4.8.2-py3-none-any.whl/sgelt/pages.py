"""
A module to build and render pages using jinja2
"""

from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import logging
from pathlib import Path

from . import filters, mdparse
from .utils import slugify, slugify_path, md, parse_md_file, get_short_uid
from .calendar import build_calendar, merge_calendars, write_calendar_file

log = logging.getLogger(__name__)


class Page:
    """A generic class to render an html page"""

    attributes = ('title', 'category', 'filepath', 'template_name',
                  'template_path', 'menu_item', 'virtual', 'html_path',
                  'out_path', 'content')

    def __init__(self, website, filename: str, menu_item: str,
                 template_name: str = '',
                 title: str = '',
                 category: str = ''):
        self.website = website
        self.conf = website.conf
        self.data = website.data
        self.filepath = Path(filename)
        self.template_name = template_name
        self.menu_item = menu_item
        self.title = title
        self.category = category
        self.rendered = 0  # number of rendered pages
        self.content = ''  # used by lunr.js

        if template_name:
            self.template_path = Path(self.template_name)
        else:
            self.template_path = self.filepath

        self.virtual = False  # A virtual article is not rendered as html
        self.html_path = self._get_html_path()
        self.path_depth = self._get_path_depth()
        self.out_path = self._get_out_path(self.conf.output_path)

    def _get_html_path(self) -> Path:
        """Return the path of the html file to be rendered"""
        if self.category == 'conférence':
            return Path('conferences') / self.filepath
        elif self.category == 'soutenance':
            return Path('soutenances') / self.filepath
        elif self.category == 'séminaire':
            return Path('seminaires') / self.filepath
        elif self.category == 'groupe de travail':
            return Path('groupes-de-travail') / self.filepath
        elif self.category == 'news':
            return Path('actualites') / self.filepath
        else:
            return slugify_path(Path(self.category) / self.filepath)

    def _get_path_depth(self) -> int:
        """Return depth of html file path"""
        return len(self.html_path.parts) - 1

    def _log_rendering(self):
        """Display a message for file to be rendered"""
        log.debug(
            f"Rendering {self.filepath} using {self.template_path} template")

    def _get_out_path(self, parent: Path) -> Path:
        """Create output path parent and return output path"""
        out_path = parent / self.html_path
        # Create parent directory if it does not exist
        out_path.parent.mkdir(parents=True, exist_ok=True)
        return out_path

    def _do_render(self):
        template = self.conf.env.get_template(self.template_path.as_posix())
        html_out = template.render(page=self,
                                   site=self.conf.site,
                                   events=self.data.events,
                                   news=self.data.news,
                                   libnews=self.data.libnews,
                                   teams=self.data.teams)
        self.out_path.write_text(html_out)
        self.rendered = 1

    def render(self):
        """Render page object into html file"""
        self._log_rendering()
        self._do_render()

    def active_tab(self, dropdown_url) -> str:
        """
        conférences.html vs conférence, soutenances.html vs soutenance, etc.
        """
        return "active" if self.html_path.as_posix() == dropdown_url else ""

    def get_index_node(self, title='', content='', anchor='',
                       date=None) -> dict:
        """
        Return a node for lunr.js index json file
        (inspired by tipue_search.py plugin for Pelican)
        """
        if title == '':
            title = self.title
        if content == '':
            content = self.content

        try:
            if date is None:
                date = self.date
            node_date = date.strftime("%d/%m/%Y")
        except AttributeError:
            node_date = ''

        if content == '':
            if self.__class__ is not Page:
                # Ignore warning for Page class
                log.warning(f"Empty content for {self.title}")
                log.warning(self)
            return

        soup_title = BeautifulSoup(title.replace("&nbsp;", " "), "html.parser")
        node_title = (
            soup_title.get_text(" ", strip=True)
            .replace("“", '"')
            .replace("”", '"')
            .replace("’", "'")
            .replace("^", "&#94;")
        )

        soup_text = BeautifulSoup(content, "html.parser")
        node_text = (
            soup_text.get_text(" ", strip=True)
            .replace("“", '"')
            .replace("”", '"')
            .replace("’", "'")
            .replace("¶", " ")
            .replace("^", "&#94;")
        )
        node_text = " ".join(node_text.split())

        if self.virtual and 'external_url' in self.metadata:
            node_url = self.metadata['external_url']
        else:
            node_url = self.html_path.as_posix()  # Real path
            node_url += anchor

        node = {
            "title": node_title,
            "text": node_text,
            "tags": self._get_tags(),
            "url": node_url,
            "date": node_date
        }

        return node

    def _get_tags(self) -> list:
        """Return a tag list for search index node"""
        return [self.category]

    def get_ical_event(self, event: dict, next_event: dict = {}) -> dict:
        """Return an ical event dict"""
        dtstart = event.get('start',  event['date'])
        if dtstart is None:
            dtstart = event['date']
        try:
            dtend = event['date_end']
        except KeyError:
            if next_event:
                dtend = next_event['start']
                if dtend is None:
                    dtend = event['date']
            else:
                dtend = dtstart + timedelta(hours=1)
        # dstamp is now
        dtstamp = datetime.combine(self.conf.site['today'],
                                   datetime.now().time())
        summary = ' - '.join(
            [item for item in (event.get('speaker'),
                               event.get('title'))
             if item])

        ical_event = {
            'summary': summary,
            'dtstart': dtstart,
            'dtend': dtend,
            'dtstamp': dtstamp,
        }
        if 'url' in self.conf.site:
            ical_event['url'] = \
                f"{self.conf.site['url']}/{self.html_path.as_posix()}"
        else:
            ical_event['url'] = self.html_path.as_posix()
        try:
            ical_event['location'] = event['place']
        except KeyError:
            pass
        try:
            ical_event['description'] = event['abstract']
        except KeyError:
            pass
        return ical_event

    def __repr__(self) -> str:
        """List all existing attributes values in a string"""

        from pprint import pformat
        s = f'\n{self.__class__.__name__}:\n'
        for name in self.attributes:
            value = getattr(self, name, '')
            s += f'  {name}: {pformat(value)}\n'
        return s


class MdPage(Page):
    """A class to convert a markdown source into an html page"""

    parser = mdparse.shortcodes.Parser(start="{{%", end="%}}", esc="\\")
    virtual = False

    def __init__(self, website, md_path: Path, metadata: dict, md_content: str,
                 template_name: str = ''):

        self.website = website
        self.conf = website.conf
        self.data = website.data
        self.filepath = md_path
        self.metadata = metadata
        if template_name:
            # template_name is passed as argument: use it
            self.template_path = Path(template_name)
        else:
            # read template_name from metadata or use default
            self.template_path = Path(self.metadata.get('template',
                                                        "article.html"))

        self.title = self.metadata['title']
        self.menu_item = self.metadata.get('menu_item', '')
        self.category = self.metadata.get('category', 'article')
        self.date = self.metadata.get('date', '')

        self.rendered = 0  # number of rendered pages

        self.html_path = self._get_html_path()
        self.path_depth = self._get_path_depth()
        self.out_path = self._get_out_path(self.conf.output_path)

        self.team_seminars = (self._get_team_seminars()
                              if self.category == 'team' else None)

        self.md_content = self._parse_shortcodes(md_content)
        self.sections, self.toc = self._get_sections_and_toc()
        self.content = self._get_content()

    def _get_sections_and_toc(self) -> tuple:
        """Return the tuple (sections, toc) from markdown content"""
        return mdparse.get_sections(self.md_content)

    def _get_content(self) -> str:
        """Return the file text from makdown content (for search index)"""
        content = self.metadata.get('description', '')
        for section in self.sections:
            if section['title']:
                content += f"{section['title']} - {section['content']}\n"
            else:
                content += f"{section['content']}\n"
        return content

    def _get_team_seminars(self) -> list:
        """
        If category is a team, return the list of seminars organized
        by the team
        """
        return [seminar for seminar in self.data.seminars
                if self.metadata['team'] in seminar['teams']
                and seminar['status'] == 'actif']

    def _parse_shortcodes(self, md_content: str) -> str:
        """Parse markdown string for shortcodes"""

        return self.parser.parse(md_content, context={'data': self.data,
                                                      'page': self})

    def _get_html_path(self) -> Path:
        """Return the path of the html file to be rendered"""
        # Convert Markdown source file path to html output file path
        abs_content_path = self.conf.content_path.resolve()
        md_parent = self.filepath.resolve().relative_to(
            abs_content_path).parent
        # Replace .md suffix by .html
        html_filename = self.filepath.stem + '.html'
        return slugify_path(md_parent / html_filename)


class NewsPage(MdPage):
    """A class to convert a news source into an html page"""

    category = 'news'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._register_news()

    def _get_href(self):
        return self.html_path.as_posix()

    def _register_news(self):
        """Append libnews dict to data.news list"""
        log.debug(f"Registering news from {self.filepath}")
        href = self._get_href()
        news = {'title': self.title,
                'date': self.metadata['date'],
                'chapo': self.metadata['description'],
                'text': self.sections,
                'external': self.virtual,
                'href': href
                }
        self.data.news.append(news)


class VirtualPage(NewsPage):
    """Abtract class for virtual news or libnews page"""
    virtual = True

    def _get_href(self):
        pass

    def _get_html_path(self):
        return self._get_href()

    def _get_out_path(self, _):
        pass

    def _get_path_depth(self):
        pass

    def render(self):
        pass


class VirtualNewsPage(VirtualPage):
    """A class to convert an external news into an html page"""

    category = 'news'

    def _get_sections_and_toc(self) -> tuple:
        """Return a tuple of None"""
        return None, None

    def _get_content(self) -> str:
        """Return the file text from markdown content (for search index)"""
        return self.metadata.get('description', self.title)

    def _get_href(self):
        return self.metadata['external_url']


class LibNewsPage(VirtualPage):

    category = 'libnews'

    def _register_news(self):
        """Append libnews dict to data.news list"""
        log.debug(f"Registering libnews from {self.filepath}")
        news = {'title': self.title,
                'slug': slugify(self.title),
                'date': self.metadata['date'],
                'text': ''.join([section['content']
                                 for section in self.sections]),
                }
        self.data.libnews.append(news)

    def get_index_node(self, *args, **kwargs):
        pass


class HomePage(Page):
    """A class to convert a markdown card into index.html"""

    index_path = Path('index.html')
    template_path = index_path
    filepath = index_path
    html_path = index_path
    category = 'homepage'
    virtual = False
    attributes = Page.attributes + ('cards',)

    def __init__(self, website, title: str):
        self.website = website
        self.conf = website.conf
        self.data = website.data
        self.title = title
        self.path_depth = self._get_path_depth()
        self.out_path = self._get_out_path(self.conf.output_path)
        self.content = ''

        self.cards = [self._get_card(md_path)
                      for md_path
                      in sorted(self.conf.content_path.glob('home/*.md'))]

    def _get_card(self, md_path: Path) -> dict:
        """
        Parse markdown file:
            - add file dependency
            - add text to content
            - return a card dict
        """
        card, md_content = parse_md_file(md_path)
        card['text'] = md.convert(md_content)
        self.content += card['text']
        return card


class EventPage(Page):
    """An abstract class to render an event page to be registered in agenda"""

    attributes = Page.attributes + ('event',)

    def __init__(self, *args, **kwargs):
        """
        Same as Page initializer except that:
        - `event` args is added
        - `filename` is generated by _get_filename()
        - `text` is initialized
        """
        self.title = kwargs['title']
        self.event = kwargs.pop('event')  # event is specific to this class
        self.text = ''
        self.date = self.event['date']
        super().__init__(filename=self._get_filename(), *args, **kwargs)

    def _register_events(self):
        """Add event to site dict"""
        self.event['category'] = self.category
        self.event['target'] = self.html_path
        self.data.events.append(self.event)

    def _get_filename(self):
        pass

    def render(self):
        """To be implemented by childs"""
        pass

    def active_tab(self, dropdown_url) -> str:
        """
        conférences.html vs conférence, soutenances.html vs soutenance, etc.
        """
        return ("active" if dropdown_url.startswith(
            self.html_path.parents[0].as_posix()) else "")


class ConferencePage(EventPage):
    """A class to render a conference page"""

    def _get_filename(self):
        """Return filename from title and article id"""
        slug = slugify(self.title)
        try:
            article_id = self.event['article']['id']
        except KeyError:
            article_id = get_short_uid()
        return f"{slug}-{article_id}.html"

    def _export_ical(self):
        """
        Export the ical file for the conference
        """

        ical_events = []
        for day in self.event['program'].values():
            # sort time_slots by date or start time
            time_slots = sorted(day['time_slots'],
                                key=lambda e: e['date']if e['start'] is None
                                else e['start'])
            for this_slot, next_slot in zip(time_slots, time_slots[1:]):
                ical_events.append(self.get_ical_event(this_slot, next_slot))
            # Add the last time_slot
            ical_events.append(self.get_ical_event(time_slots[-1]))

        prodid = (f"\
-//{self.conf.site['calendar']['organization']}//conferences//"
                  f"{self.title}//FR")
        ical_content = build_calendar(prodid, ical_events)
        self.ical_url = write_calendar_file(self._get_filename(),
                                            self.conf,
                                            ical_content)

    def render(self):
        """Render after converting spip text into html"""
        self._log_rendering()
        self._register_events()
        try:
            # data is from Spip
            self.text = md.convert(self.event['article']['text'])
        except KeyError:
            # data is from Indico
            self.text = md.convert(self.event['description'])
        self.content += self.text
        for day in self.event['program'].values():
            for time_slot in day['time_slots']:
                try:
                    # If no speaker then pass
                    self.content += f"\n{time_slot['speaker']} - "
                    self.content += f"{time_slot['title']} - "
                    self.content += time_slot['abstract']
                except KeyError:
                    pass
        self._export_ical()
        self._do_render()


class DefensePage(EventPage):
    """A class to render a defense page"""

    def _get_filename(self):
        """Return filename from title"""
        slug = slugify(f"soutenance-{self.title}")
        return f"{slug}.html"

    @staticmethod
    def format_abstract(s):
        """Add line return in html"""
        return s.replace('\n', '<br>\n')

    @staticmethod
    def format_jury(s):
        """Add line return in html"""
        new = '<ul>\n'
        new += '\n'.join([f'<li>{line}</li>' for line in s.split('\n')])
        new += '</ul>\n'
        return new

    def render(self):
        """Render after converting spip text into html"""
        self._log_rendering()
        self._register_events()
        spip_jury = self.event.get('jury')
        spip_abstract = self.event.get('abstract')
        if spip_jury:
            self.jury = self.format_jury(spip_jury)
            self.content += f"{self.jury}\n"
        if spip_abstract:
            self.abstract = self.format_abstract(spip_abstract)
            self.content += f"{self.abstract}\n"
        self.defense_type = self.event.get('theme', 'thèse')
        self.speaker = self.event['speaker']
        self.content += f"{self.speaker}\n"
        self._do_render()


class IndexPage(Page):
    """A class to render a paginated page"""

    attributes = Page.attributes + ('ical_url', 'is_subpage', 'paginator')

    def __init__(self, *args, is_subpage=False, **kwargs):
        self.is_subpage = is_subpage
        self.title = kwargs['title']
        self.category = kwargs.get('category', '')
        # Get class-specific args and remove them from kwargs
        self.events = kwargs.pop('events')
        self.name = kwargs.pop('name', None)
        self.paginator = kwargs.pop('paginator', None)
        self.seminar = kwargs.pop('seminar', None)
        # Get filename from named arg or from method
        if 'filename' not in kwargs:
            kwargs['filename'] = self._get_filename()
        else:
            kwargs['filename'] = slugify(kwargs['filename'])
        super().__init__(*args, **kwargs)
        self.content = self.title

        if not self.is_subpage:
            self._paginate()
        else:
            self.subpages = None

    def _paginate(self):
        names = self._get_page_names()

        if len(names) > 1:  # Do paginate
            self.paginator = Paginator(names, str(self.filepath))
            self.subpages = []
            # Loop on subpages
            for name in names:
                self.name = name  # needed by _register_events()

                subpage = IndexPage(
                    website=self.website,
                    menu_item=self.menu_item,
                    template_name=self.template_name,
                    title=self.title,
                    category=self.category,
                    name=name,
                    paginator=self.paginator,
                    events=self.events,  # used only by SeminarPage
                    seminar=self.seminar,
                    is_subpage=True
                )
                subpage._register_events()
                self.subpages.append(subpage)
        else:
            self._register_events()
            self.paginator = None
            self.subpages = None

    def _get_filename(self):
        """Return filename from paginator"""
        return self.paginator.get_filename(self.name)

    def active_tab(self, dropdown_url) -> str:
        """html_path corresponds to dropdown_url"""
        if self.category:
            return EventPage.active_tab(self, dropdown_url)
        else:
            return "active" if self.html_path.as_posix() == dropdown_url \
                else ""

    def _get_page_names(self):
        """Return a list of page names"""
        year_set = set((event['date'].year for event in self.events))
        years = sorted(list(year_set), reverse=True)
        # Find if there are events to come
        add_to_come = False
        # Collect list of years
        collected_years = []
        for event in self.events:
            if event['date'].date() >= self.conf.site['today']:
                # there is at least one future event
                add_to_come = True
            else:
                collected_years.append(event['date'].year)
        years = sorted(list(set(collected_years)), reverse=True)
        return ['À venir'] + years if add_to_come else years

    def _register_events(self):
        """
        For conferences and defenses, the event is already registered, so
        register only seminaires
        """
        if self.category in {'séminaire', 'groupe de travail', 'colloquium'}:
            for sem_event in self.events:
                # Register event if there is no pagination
                # or if it belongs to current page
                if filters.event_selector(sem_event, self):
                    sem_event['category'] = self.category
                    sem_event['target'] = self.html_path
                    sem_event['theme'] = self.seminar['full_title']
                    sem_event['slug'] = slugify(sem_event['title'])
                    self.data.events.append(sem_event)

    def render(self):
        log.debug(f"Rendering {self.filepath}")
        if self.subpages:
            for subpage in self.subpages:
                subpage.render()
                self.rendered += subpage.rendered  # Increment counter
        else:
            super().render()


class NewsIndexPage(IndexPage):
    """A class to render a paginated page"""

    filename = "index.html"
    category = "news"
    title = "Actualités"
    template_name = "actualites.html"
    virtual = False

    def __init__(self, website, menu_item=None):
        """
        Only for news
        """
        self.website = website
        self.menu_item = menu_item
        self.conf = website.conf
        self.data = website.data
        self.news = self._get_news()
        self.filepath = Path(self.filename)
        self.template_path = Path(self.template_name)
        self.rendered = 0
        names = self._get_page_names()
        self.html_path = Path(self.filename)
        self.path_depth = self._get_path_depth()
        self.out_path = self._get_out_path(self.conf.output_path)
        self.content = self.title

        if len(names) > 1:  # Do paginate
            self.paginator = Paginator(names, self.filename)
            self.subpages = []
            # Loop on subpages
            for name in names:
                subpage = NewsIndexSubPage(
                    website=self.website,
                    name=name,
                    title=self.title,
                    template_name=self.template_name,
                    paginator=self.paginator,
                    category=self.category,
                    menu_item=self.menu_item,
                )
                self.subpages.append(subpage)
        else:
            self.paginator = None
            self.subpages = None

    def _get_news(self):
        """Return the list of news"""
        return self.data.news

    def _get_page_names(self):
        """Return a list of page names"""
        year_set = set((news['date'].year for news in self.news))
        years = sorted(list(year_set), reverse=True)
        # Find if there are recent news
        recent = False
        # Collect list of years
        collected_years = []
        for news in self.news:
            if filters.recent_news(news, self.conf.site):
                # there is at least one future event
                recent = True
            else:
                collected_years.append(news['date'].year)
        years = sorted(list(set(collected_years)), reverse=True)
        return ['Récentes'] + years if recent else years


class NewsIndexSubPage(IndexPage):

    subpages = None

    def __init__(self, website, name, title, template_name, paginator,
                 category, menu_item):
        self.name = name
        self.paginator = paginator
        Page.__init__(self,
                      website,
                      title=title,
                      filename=self._get_filename(),
                      menu_item=menu_item,
                      template_name=template_name,
                      category=category)


class LibNewsIndexPage(NewsIndexPage):
    """A class to render a paginated page"""

    filename = "actualites-bib.html"
    category = "libnews"
    title = "Actualités de la bibliothèque"
    template_name = "actualites-bib.html"

    def _get_news(self):
        """Return the list of news"""
        return self.data.libnews

    def get_index_node(self) -> list:
        """Overload get_index_node() for libnews pages"""

        def add_node(index_nodes, page, news):
            """Add a node to lunr json"""
            index_node = page.get_index_node(
                title=f"{self.title} - {news['title']}",
                content=news['text'],
                date=news['date'],
                anchor=f"#{news['slug']}")
            index_nodes.append(index_node)

        index_nodes = []
        for news in self.news:
            if self.subpages:
                for subpage in self.subpages:
                    if filters.news_selector(news, subpage):
                        add_node(index_nodes, subpage, news)
            else:
                add_node(index_nodes, super(), news)

        return index_nodes


class SeminarPage(IndexPage):
    """A class to render a seminar page"""

    def _get_filename(self):
        """Return filename from seminar type and title"""
        seminar_type = self.seminar['type']
        slug = slugify(f"{seminar_type}-{self.title}")
        return f"{slug}.html"

    def _get_html_path(self) -> Path:
        """Return the path of the html file to be rendered"""
        html_path = super()._get_html_path()
        # Register seminar page for SeminarTopIndexPage
        self.seminar['html_path'] = html_path
        return html_path

    def _export_ical(self):
        """
        Export the ical file for the seminar
        Limit to less than one-year old events
        """
        ical_events = []
        for sem_event in self.events:
            if (sem_event['date'].date() >=
                    self.conf.site['today'] - timedelta(days=365)):
                ical_events.append(self.get_ical_event(sem_event))

        prodid = (f"\
-//{self.conf.site['calendar']['organization']}//{self.seminar['type']} "
                  f"{self.title}//FR")
        ical_content = build_calendar(prodid, ical_events)
        self.ical_url = write_calendar_file(self._get_filename(),
                                            self.conf,
                                            ical_content)

    def get_index_node(self) -> list:
        """Overload get_index_node() for seminar pages"""

        def add_node(index_nodes, page, sem_event):
            """Add a node to lunr json"""
            sem_event['slug'] = slugify(sem_event['title'])
            index_node = page.get_index_node(
                title=f"{self.title} - {sem_event['title']}",
                content=f"{sem_event['speaker']} - {sem_event['abstract']}",
                date=sem_event['date'],
                anchor=f"#{sem_event['slug']}")
            index_nodes.append(index_node)

        index_nodes = []
        for sem_event in self.events:
            if self.subpages:
                for subpage in self.subpages:
                    if filters.event_selector(sem_event, subpage):
                        add_node(index_nodes, subpage, sem_event)
            else:
                add_node(index_nodes, super(), sem_event)

        return index_nodes

    def render(self):
        """Export ical file before rendering"""
        if 'calendar' in self.conf.site and self.seminar['status'] == 'actif':
            self._export_ical()
            if self.subpages:  # Populate subpages with ical_url
                for subpage in self.subpages:
                    subpage.ical_url = self.ical_url
        return super().render()


class TopIndexPage(Page):
    """
    An abstract class to build the seminars and work groups top index page
    (actifs/passés)
    """

    event_types: list[str] = []
    event_title = ''
    event_dir = ''

    def __init__(self, *args, **kwargs):
        # Get class-specific args
        # Filter events by event_type
        self.seminars = [event for event in kwargs.pop('seminars')
                         if event['type'].lower() in self.event_types]
        self.status = kwargs.pop('status')
        # Build filename based on status
        kwargs['filename'] = ('index.html' if self.status == 'actif'
                              else 'passes.html')
        # Call mother class initializer
        super().__init__(*args, **kwargs)
        self.content = self.title
        self.category = f"{self.event_title} {self.status}s"

    def _get_html_path(self) -> Path:
        """Return the path of the html file to be rendered"""
        return Path(self.event_dir) / self.filepath

    def active_tab(self, dropdown_url) -> str:
        """
        conférences.html vs conférence, soutenances.html vs soutenance, etc.
        """
        return ("active" if self.html_path.parts[0] == Path(dropdown_url).stem
                else "")


class SeminarTopIndexPage(TopIndexPage):
    """A class to build the seminars top index page"""

    event_types = ['séminaire', 'colloquium']
    event_title = 'Séminaires'
    event_dir = 'seminaires'

    def _export_ical(self):
        prodid = (f"-//{self.conf.site['calendar']['organization']}"
                  f"//{self.event_title.lower()}//FR")

        ics_file_paths = Path(self.conf.output_path / 'cal').glob('**/*.ics')
        ical_content = merge_calendars(prodid, ics_file_paths,
                                       {'Séminaire', 'Colloquium'})
        self.ical_url = write_calendar_file(f'{self.event_title.lower()}.ics',
                                            self.conf,
                                            ical_content)

    def render(self):
        if 'calendar' in self.conf.site and self.status == 'actif':
            self._export_ical()
        super().render()


class WorkGroupTopIndexPage(TopIndexPage):
    """A class to build the work groups top index page"""

    event_types = ['groupe de travail']
    event_title = 'Groupes de travail'
    event_dir = 'groupes-de-travail'


class Paginator:
    """
    An object to find filename and next/previous elements
    in year list
    """

    def __init__(self, names: list, basefilename: str):
        """
        names: the list of names that will be rendered as sub-pages
        example.html will paginated to example-2019.html, example-2018.html,
        etc.
        """
        self.names = names
        self.basefilename = basefilename

    def get_filename(self, name: int) -> str:
        """Return paginated filename"""
        if name == self.names[0]:
            # Most recent year keeps its original filename
            return self.basefilename
        else:
            return f"{self.basefilename[:-5]}-{name}.html"

    def has_next(self, name):
        """True if current element has a right neighbour"""
        return not name == self.names[-1]

    def has_previous(self, name):
        """True if current element has a lest neighbour"""
        return not name == self.names[0]

    def next_filename(self, name):
        name_index = self.names.index(name)
        if self.has_next(name):
            return self.get_filename(self.names[name_index + 1])
        else:
            return '#'

    def previous_filename(self, name):
        name_index = self.names.index(name)
        if self.has_previous(name):
            return self.get_filename(self.names[name_index - 1])
        else:
            return '#'

    def __repr__(self):
        return f"{self.names} - {self.basefilename}"
