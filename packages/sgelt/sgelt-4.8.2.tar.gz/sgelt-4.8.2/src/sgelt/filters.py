import types
from datetime import timedelta
import jinja2

from .utils import slugify


def exclude_events(events):
    """Exclude events whose speaker is TBA"""
    for event in events:
        try:
            speaker = event['speaker']
            if 'tba' not in speaker.lower().split():
                yield event
        except KeyError:
            yield event


def filter_titles(events):
    """If event title is in to_filter, modify it to 'À venir'"""
    title_filter = 'tba', 'à venir', 'à confirmer'
    for event in events:
        if event['title'].lower() in title_filter:
            event['title'] = 'À venir'
        yield event


def sort_by_date(events, reverse=False) -> list:
    """Revert events sort by date"""
    event_list = list(events) if isinstance(
        events, types.GeneratorType) else events
    return sorted(event_list, key=lambda e: e['date'], reverse=reverse)


@jinja2.pass_context
def homepage(context, events) -> list:
    """
    - exclude TBA authors
    - filter TBA titles
    - (reverse) sort by date
    - keep only 6 first events
    """
    site = context['site']
    selected_events = exclude_events(events)
    filtered_title_events = filter_titles(selected_events)
    sorted_events = sort_by_date(filtered_title_events)
    next_events = [e for e in sorted_events
                   if e.get('end', e['date']).date() >= site['today']]
    return next_events[:6]


@jinja2.pass_context
def homepage_news(context, site_news):
    """
    - keep only recent news
    - (reverse) sort by date
    """
    site = context['site']
    selected_news = (news for news in site_news if recent_news(news, site))
    return sort_by_date(selected_news, reverse=True)[:5]


@jinja2.pass_context
def agenda(context, events):
    """
    - keep same category
    - keep same year
    - exclude TBA authors
    - filter TBA titles
    - (reverse) sort by date
    """
    page = context['page']
    site = context['site']
    if page.category:
        category_selection = (
            event for event in events if event['category'] == page.category)
    else:
        category_selection = (event for event in events if event['category'])

    if page.name:
        name_selection = (
            event for event in category_selection
            if page_name(event, site) == page.name
        )
    else:
        name_selection = category_selection

    author_selection = exclude_events(name_selection)
    filter_titles_events = filter_titles(author_selection)
    sorted_events = sort_by_date(filter_titles_events)
    return sorted_events


def event_date_time(event, weekday=False, sep=':') -> str:
    """Return event date(s) (and time)"""

    start = event['date']
    try:
        end = event['end']
        if end != start:
            if end.month == start.month:
                return f"Du {start.day} au {end.day} {end.strftime('%B %Y')}"
            else:
                return (f"Du {start.day} {start.strftime('%B')} au {end.day} "
                        f"{end.strftime('%B %Y')}")
        else:
            return f"""{start.strftime(
                f"{'%A ' if weekday else ''}%-d %B %Y").capitalize()}"""

    except KeyError:
        date_time = start.strftime(
            f"{'%A ' if weekday else ''}%-d %B %Y").capitalize()
        if start.strftime("%H:%M") != '00:00':
            format = f"%H{sep}%M"
            date_time += f" - {start.strftime(format)}"
        return date_time


def categ_to_target(event):
    """Return the target corresponding to event category"""
    category = event['category']
    if category == 'groupe de travail':
        return "groupes-de-travail"
    else:
        return f"{slugify(category)}s"


@jinja2.pass_context
def url(context: dict, value: str) -> str:
    """Return the relative url"""
    if value.startswith(('http://', 'https://', '#')):
        return value
    else:
        return context['page'].path_depth * '../' + value


def external_url(value: str) -> str:
    """Add attributes to external URLs a tags"""
    if value.startswith(('http://', 'https://')):
        return '\
referrerpolicy="no-referrer" rel="noopener noreferrer" target="_blank"'
    else:
        return ''


def page_name(event, site: dict):
    """
    Return the page name that event belongs to:
    "À venir", "2020", "2019", etc.
    """
    event_date = event['date'].date()
    return "À venir" if event_date >= site['today'] else event_date.year


def event_selector(event, page):
    """Return true if event should be display in page"""
    site = page.conf.site
    return (not page.paginator
            or page.name == page_name(event, site))


def recent_news(news: dict, site: dict) -> bool:
    """Return True if news is less than 180 days ago"""
    try:
        date = news['date'].date()
    except AttributeError:
        date = news['date']
    return date >= site['today'] - timedelta(days=180)


def news_page_name(news, site: dict):
    """
    Return the page name that event belongs to:
    "Récentes", "2020", "2019", etc.
    """
    # Handle both datetime and date objects
    try:
        year = news['date'].date().year
    except AttributeError:
        year = news['date'].year
    return "Récentes" if recent_news(news, site) else year


def news_selector(news, page):
    """Return true if news should be display in page"""
    return (not page.paginator
            or page.name == news_page_name(news, page.website.conf.site))


@jinja2.pass_context
def news_page(context, site_news):
    """
    - keep same year
    - (reverse) sort by date
    """
    page = context['page']
    site = context['site']
    if page.paginator:
        name_selection = (news for news in site_news
                          if news_page_name(news, site) == page.name)
    else:
        name_selection = site_news
    return sort_by_date(name_selection, reverse=True)


@jinja2.pass_context
def dropdown_items(context, nav_items):
    """Return the dropdown_items if item is a dict else {}"""
    page = context['page']
    nav_item = nav_items[page.menu_item]
    return nav_item if isinstance(nav_item, dict) else {}


def get_fullname(teams: dict, shortname: str) -> str:
    """Return fullname from shortname"""
    try:
        return teams[shortname]['fullname']
    except KeyError:
        # team entry does not belongs to research teams list
        return shortname


def real_teams(sem_teams: list) -> bool:
    """Return True if team is not in exclude names"""
    return bool(sem_teams) and sem_teams[0].upper() not in {
        'COLLOQUIUM', 'ENTR', 'AUTRE'}


@jinja2.pass_context
def teams(context, sem_teams) -> str:
    """
    Format team names such as:
    Team1,
    Team1 and Team2
    Team1, Team2 and Team3
    """

    t_dict = context['teams']

    if sem_teams:
        if len(sem_teams) == 1:
            return get_fullname(t_dict, sem_teams[0])
        else:
            return "{} et {}".format(', '.join(get_fullname(t_dict, team)
                                               for team in sem_teams[:-1]),
                                     get_fullname(t_dict, sem_teams[-1]))
    else:
        return ''


@jinja2.pass_context
def organizing_teams(context, sem_teams) -> str:
    """
    Format team names such as:
    organisé par l'équipe Team1,
    organisé par les équipes Team1 et Team2
    """

    if not real_teams(sem_teams):
        return ''

    t_dict = context['teams']

    def link_team(team: str) -> str:
        """Return a html link with the team fullname"""
        if team in t_dict:
            target = url(context, f"teams/{team.lower()}.html")
            return f'''\
<a href="{target}">{get_fullname(t_dict, team)}</a>\
'''
        else:
            return team

    if sem_teams:
        if len(sem_teams) == 1:
            return f"organisé par l'équipe {link_team(sem_teams[0])}"
        else:
            return "organisé par les équipes {} et {}".format(
                ', '.join(link_team(team) for team in sem_teams[:-1]),
                link_team(sem_teams[-1]))
    else:
        return ''
