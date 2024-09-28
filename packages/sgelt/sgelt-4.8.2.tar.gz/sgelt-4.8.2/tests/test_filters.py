from datetime import datetime, timedelta
from freezegun import freeze_time
import jinja2
import pytest

from common import freeze_today
from sgelt import filters


@pytest.fixture
@freeze_time(freeze_today)
def base_events() -> list:
    """A Mockup list of events"""

    today = datetime.today()
    yesterday = today - timedelta(1)
    tomorrow = today + timedelta(1)
    pretty_old = today - timedelta(120)
    very_old = datetime(2000, 1, 1)
    future_date = today + timedelta(180)
    events = [
        {'date': today,
         'title': 'Today',
         'category': 'conférence'},
        {'date': tomorrow,
         'title': 'Tomorrow',
         'category': 'séminaire'},
        {'date': yesterday,
         'title': 'Yesterday',
         'category': 'conférence'},
        {'date': pretty_old,
         'title': 'Pretty Old',
         'category': 'séminaire'},
        {'date': very_old,
         'title': 'Very Old',
         'category': 'conférence'},
        {'date': future_date,
         'title': 'Future',
         'category': 'conférence'},
        {'date': tomorrow,
         'title': 'tba',
         'category': 'séminaire'},
        {'date': tomorrow,
         'title': 'à venir',
         'category': ''},
    ]
    return events


def get_titles(events: list) -> list:
    """Return list of title values from list of event dicts"""
    return [event['title'] for event in events]


def check_templating(source: str, expected: str, **kwargs):
    """Assert that rendered template source corresponds to expected string"""
    env = jinja2.Environment(
        loader=jinja2.DictLoader({'test.html': source})
    )
    env.filters['agenda'] = filters.agenda
    env.filters['dropdown_items'] = filters.dropdown_items
    env.filters['categ_to_target'] = filters.categ_to_target
    env.filters['event_selector'] = filters.event_selector
    env.filters['news_page'] = filters.news_page
    template = env.get_template('test.html')

    html_out = template.render(**kwargs)
    if kwargs.get('print_out'):
        print(html_out)
    assert html_out == expected


def test_homepage(miniwebsite, base_events):

    context = {'site': miniwebsite.conf.site}
    homepage_events = filters.homepage(context, base_events)
    assert get_titles(homepage_events) == ['Today', 'Tomorrow', 'À venir', 'À venir',
                                           'Future']


def test_recent_news(miniwebsite, base_events):
    selected_news = (news for news in base_events
                     if filters.recent_news(news, miniwebsite.conf.site))
    assert get_titles(selected_news) == ['Today', 'Tomorrow', 'Yesterday',
                                         'Pretty Old', 'Future', 'tba',
                                         'à venir']


def test_homepage_news(miniwebsite, base_events):

    context = {'site': miniwebsite.conf.site}

    sorted_news = filters.homepage_news(context, base_events)
    assert get_titles(sorted_news) == ['Future',
                                       'Tomorrow',
                                       'tba',
                                       'à venir',
                                       'Today']


def test_agenda(base_events, miniwebsite):
    class TestPage:
        """A mock class for a Page"""
        category = 'conférence'
        name = None
        conf = miniwebsite.conf

    source = """\
{%- for event in events | agenda -%}
{{ event.title }}
{% endfor -%}
"""
    expected = """\
Very Old
Yesterday
Today
Future
"""

    check_templating(source, expected, page=TestPage, events=base_events,
                     site=TestPage.conf.site)


def test_url():
    class TestPage:
        """A mock class for a Page"""
        path_depth = 0

    context = {'page': TestPage()}

    value = "spam.html"
    assert filters.url(context, value) == value
    context['page'].path_depth = 1
    assert filters.url(context, value) == '../' + value
    context['page'].path_depth = 2
    assert filters.url(context, value) == '../../' + value

    # Test with external URL or anchor link

    def check_no_prefix(value: str):
        context['page'].path_depth = 0
        assert filters.url(context, value) == value
        context['page'].path_depth = 1
        assert filters.url(context, value) == value

    check_no_prefix("http://fake.fr")
    check_no_prefix("https://fake.fr")
    check_no_prefix("#anchor")


def test_external_url():

    # Expect empty string
    assert filters.external_url("spam.md") == ''
    assert filters.external_url("egg.html") == ''

    # Expect additional attributes
    s = '\
referrerpolicy="no-referrer" rel="noopener noreferrer" target="_blank"'
    assert filters.external_url("https://fake.fr") == s
    assert filters.external_url("http://fake.fr") == s


@freeze_time(freeze_today)
def test_page_name(miniwebsite):
    today = datetime.today()
    yesterday = today + timedelta(days=-1)
    this_year = yesterday.year
    tomorrow = today + timedelta(days=1)
    tomorrow_event = {'date': tomorrow}
    assert filters.page_name(tomorrow_event,
                             site=miniwebsite.conf.site) == 'À venir'
    yesterday_event = {'date': yesterday}
    assert filters.page_name(yesterday_event,
                             site=miniwebsite.conf.site) == this_year


def test_dropdown_items(miniwebsite):

    class TestPage:
        """A mock class for a Page"""
        menu_item = 'Agenda'

    source = """\
{%- for item, url in (site.nav_items | dropdown_items).items() -%}
<li>
    <a href="{{ url }}">{{ item }}</a>
</li>
{% endfor %}
"""
    # Dropdown menu
    expected = """\
<li>
    <a href="a_venir.html">À venir</a>
</li>
<li>
    <a href="conferences/">Conférences</a>
</li>
<li>
    <a href="seminaires/">Séminaires</a>
</li>
<li>
    <a href="groupes-de-travail/">Groupes de travail</a>
</li>
<li>
    <a href="soutenances/">Soutenances</a>
</li>
"""

    check_templating(source, expected, page=TestPage,
                     site=miniwebsite.conf.site)

    # Single menu: no dropdown menu
    TestPage.menu_item = '<i class="material-icons">search</i>'
    check_templating(source, '', page=TestPage, site=miniwebsite.conf.site)


def test_categ_to_target(miniwebsite, base_events):
    class TestPage:
        """A mock class for a Page"""
        category = None
        name = None

    source = """\
{%- for event in events | agenda -%}
{{ event | categ_to_target }}
{% endfor -%}
"""
    expected = """\
conferences
seminaires
conferences
conferences
seminaires
seminaires
conferences
"""
    check_templating(source, expected, page=TestPage, events=base_events,
                     site=miniwebsite.conf.site)


def test_event_selector(base_events, miniwebsite):

    class TestPage:
        """A mock class for a Page"""
        category = None
        name = None
        events = base_events
        paginator = None
        conf = miniwebsite.conf

    # Test with no paginator
    source = """\
{%- for event in page.events if event|event_selector(page) -%}
{{ event.title }}
{% endfor -%}
"""
    expected = """\
Today
Tomorrow
Yesterday
Pretty Old
Very Old
Future
tba
à venir
"""
    check_templating(source, expected, page=TestPage, events=base_events)

    # Test with paginator - page.name = "À venir"
    TestPage.paginator = True
    TestPage.name = "À venir"
    expected = """\
Today
Tomorrow
Future
tba
à venir
"""
    check_templating(source, expected, page=TestPage, events=base_events)

    # Test with paginator - page.name = 2000
    TestPage.name = 2000
    expected = """\
Very Old
"""
    check_templating(source, expected, page=TestPage, events=base_events)


def test_sort_by_date(base_events):

    sorted_events = filters.sort_by_date(base_events)
    assert get_titles(sorted_events) == [
        'Very Old', 'Pretty Old', 'Yesterday', 'Today', 'Tomorrow',
        'tba', 'à venir', 'Future']


def test_news_page(miniwebsite, base_events):

    class TestPage:
        """A mock class for a Page"""
        category = None
        name = None
        events = base_events
        paginator = None

    source = """\
{%- for actu in news | news_page -%}
{{ actu.title }}
{% endfor -%}
"""

    # Test with no paginator
    expected = """\
Future
Tomorrow
tba
à venir
Today
Yesterday
Pretty Old
Very Old
"""
    check_templating(source, expected, page=TestPage, news=base_events,
                     site=miniwebsite.conf.site)

    # Test with paginator - page.name = "Récentes"
    TestPage.paginator = True
    TestPage.name = "Récentes"
    expected = """\
Future
Tomorrow
tba
à venir
Today
Yesterday
Pretty Old
"""
    check_templating(source, expected, page=TestPage, news=base_events,
                     site=miniwebsite.conf.site)

    # Test with paginator - page.name = "Récentes"
    TestPage.paginator = True
    TestPage.name = 2000
    expected = """\
Very Old
"""
    check_templating(source, expected, page=TestPage, news=base_events,
                     site=miniwebsite.conf.site)


def test_real_teams():
    assert not filters.real_teams([])
    assert filters.real_teams(['AGA'])
    assert not filters.real_teams(['COLLOQUIUM'])
    assert not filters.real_teams(['colloquium'])
    assert not filters.real_teams(['AUTRE'])
    assert not filters.real_teams(['ENTR'])


def test_teams(miniwebsite):
    data = {'teams': miniwebsite.data.teams}
    assert filters.teams(data, []) == ''
    assert filters.teams(data, ['RA']) == 'Really Amazing'
    assert filters.teams(data, ['SUSU', 'WG']) == 'Super Sub et Wonder Great'
    assert (filters.teams(data, ['SUSU', 'WG', 'RA'])
            == 'Super Sub, Wonder Great et Really Amazing')
    assert filters.teams(data, ['Not a team']) == 'Not a team'


def test_organizing_teams(miniwebsite):
    class TestPage:
        """A mock class for a Page"""
        path_depth = 1

    page = TestPage()
    data = {'teams': miniwebsite.data.teams, 'page': page}

    assert filters.organizing_teams(data, ['COLLOQUIUM']) == ''

    assert filters.organizing_teams(data, ['Old team']) == """\
organisé par l'équipe Old team"""

    assert filters.organizing_teams(data, ['RA']) == """\
organisé par l'équipe <a href="../teams/ra.html">Really Amazing</a>"""

    assert filters.organizing_teams(data, ['TU', 'WG']) == ("""\
organisé par les équipes <a href="../teams/tu.html">Totally Unbelievable</a>"""
                                                            """\
 et <a href="../teams/wg.html">Wonder Great</a>""")

    assert filters.organizing_teams(data, ['SUSU', 'WG', 'RA']) == ("""\
organisé par les équipes <a href="../teams/susu.html">Super Sub</a>,"""
                                                                    """\
 <a href="../teams/wg.html">Wonder Great</a> et"""
                                                                    """\
 <a href="../teams/ra.html">Really Amazing</a>""")
