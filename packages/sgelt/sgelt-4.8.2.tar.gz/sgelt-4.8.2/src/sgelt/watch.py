"""
Watch for changes in content/ and payload dirs and rebuild site
using watchdog
"""

import time
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import PatternMatchingEventHandler
import logging

from sgelt import sgelt, config

log = logging.getLogger(__name__)


def watch(conf):
    """Build once and rebuild website everytime content/ changes"""

    class BuilderEventHandler(LoggingEventHandler):
        def on_modified(self, event):
            super().on_modified(event)
            sgelt.copy_and_build(conf)

    class CopyEventHandler(LoggingEventHandler):
        def on_modified(self, event):
            super().on_modified(event)
            log.info("Copying payload")
            website.copy_payload()

    class JsonFilesHandler(PatternMatchingEventHandler, BuilderEventHandler):
        pass

    class ConfEventHandler(PatternMatchingEventHandler, LoggingEventHandler):
        def on_modified(self, event):
            super().on_modified(event)
            conf_kwargs = conf.save_args()
            newconf = config.Config(**conf_kwargs)
            newconf.load()
            website = sgelt.Website(newconf)
            website.build()

    observer = Observer()
    # Watch for content/
    observer.schedule(BuilderEventHandler(), conf.content_path,
                      recursive=True)
    # Watch for theme/templates/
    observer.schedule(BuilderEventHandler(), conf.theme_path / "templates",
                      recursive=True)

    # watch for json agenda path
    observer.schedule(
        JsonFilesHandler(patterns=[conf.json_agenda_path.as_posix()]),
        conf.json_agenda_path.parent)

    # watch for json team path
    observer.schedule(
        JsonFilesHandler(patterns=[conf.json_teams_path.as_posix()]),
        conf.json_teams_path.parent)

    # watch for config path
    observer.schedule(
        ConfEventHandler(patterns=[conf.config_path.as_posix()]),
        conf.config_path.parent)

    # Watch for payload
    for path in conf.static_payload:
        observer.schedule(CopyEventHandler(), conf.theme_path / path,
                          recursive=True)

    observer.start()
    try:
        # Build website at first
        website = sgelt.Website(conf)
        website.build()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        log.info("Stop watching")
        observer.stop()
    observer.join()
