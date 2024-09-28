"""
A module to export iCalendar events
"""

from icalendar import Calendar, Event, vText
import logging
from pathlib import Path
import pytz
import random
import re
import uuid
import urllib.parse

from sgelt.utils import slugify

log = logging.getLogger(__name__)

rd = random.Random()
rd.seed(0)


def build_calendar(prodid: str, ical_events: list) -> str:
    """
    Return a string containing the iCalendar events
    """

    cal = Calendar()
    cal.add('prodid', prodid)
    cal.add('version', '2.0')

    tz = pytz.timezone('Europe/Paris')

    for ical_event in ical_events:
        event = Event()
        event.add('summary', ical_event['summary'])
        event.add('dtstart', tz.localize(ical_event['dtstart']).astimezone(tz))
        event.add('dtend', tz.localize(ical_event['dtend']).astimezone(tz))
        event.add('dtstamp', ical_event['dtstamp'])
        try:
            event['uid'] = ical_event['uuid']
        except KeyError:
            event['uid'] = str(uuid.UUID(int=rd.getrandbits(128)))
        try:
            event['location'] = vText(ical_event['location'])
        except KeyError:
            pass
        try:
            event['description'] = vText(ical_event['description'])
        except KeyError:
            pass
        try:
            # Encode URL for Apple Calendar
            event['url'] = vText(urllib.parse.quote(ical_event['url'],
                                                    safe='/:'))
        except KeyError:
            pass
        event.add('priority', 5)
        cal.add_component(event)

    return cal.to_ical().decode('UTF-8')


def merge_calendars(prodid: str, sem_calendar_paths: list,
                    event_types: set) -> str:
    """
    Read a list of seminars iCalendar files and merge them into
    a single iCalendar file
    """
    cal = Calendar()
    cal.add('prodid', prodid)
    cal.add('version', '2.0')

    for calendar_path in sorted(sem_calendar_paths):
        with open(calendar_path) as f:
            sem_cal = Calendar.from_ical(f.read())
        # Merge only seminars and Colloquium
        pattern = r"^-\/\/.*\/\/((" + "|".join(event_types) + r") .*)\/\/.*$"
        m = re.match(pattern, sem_cal['prodid'])
        if m:
            summary_prefix = m.group(1)
            for event in sem_cal.walk(name='VEVENT'):
                # Prepend seminar title to event summary
                event['summary'] = f"{summary_prefix} - {event.get('summary')}"
                cal.add_component(event)

    return cal.to_ical().decode('UTF-8')


def write_calendar_file(filename: str, conf,
                        ical_content: str) -> str:
    """
    Write calendar content to an .ics file and return encoded url
    """
    ical_filepath = 'cal' / Path(slugify(filename)).with_suffix('.ics')
    ical_outpath = conf.output_path / ical_filepath
    log.debug(f"Export ical file to {ical_outpath}")
    # Create parent directory if not exists
    ical_outpath.parent.mkdir(exist_ok=True, parents=True)
    ical_outpath.write_text(ical_content)
    if 'url' in conf.site:
        ical_url = \
            f"{conf.site['url']}/{ical_filepath}"
    else:
        ical_url = ical_outpath.as_posix()
    return urllib.parse.quote(ical_url, safe='/:')
