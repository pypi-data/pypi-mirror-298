"""Provide an http server and watch for changes using livereload"""

from livereload import Server
import logging

from . import sgelt, config, utils

log = logging.getLogger(__name__)


class MyServer(Server):
    """A livereload server capable of rebuilding the site"""

    def __init__(self, conf: config.Config):
        self.conf = conf
        self.host = "127.0.0.1"
        self.port = utils.get_socket_port()
        self.conf.site['url'] = f"http://{self.host}:{self.port}"
        log.info(f"Using site url: {self.conf.site['url']}")
        super().__init__()

    def serve(self, browser: bool, *args, **kwargs):
        """Serve and open browser if browser == True"""
        if browser:
            kwargs['open_url_delay'] = 0
        kwargs['root'] = self.conf.output_path
        kwargs['host'] = self.host
        kwargs['port'] = self.port
        super().serve(*args, **kwargs)

    def watch(self):
        """Watch for directories and rebuild site"""
        website = sgelt.Website(self.conf)
        website.build()

        def copy_and_build():
            """A local version without parameter"""
            sgelt.copy_and_build(self.conf)

        def build():
            """Instantiate a website and build pages"""
            website = sgelt.Website(self.conf)
            website.build_pages()

        def read_conf_and_build():
            """Read config.yml again and build site"""
            conf_kwargs = self.conf.save_args()
            self.conf = config.Config(**conf_kwargs)
            self.conf.load()
            website = sgelt.Website(self.conf)
            website.build()

        # watch for content path
        super().watch(f'{self.conf.content_path}/**/*',
                      copy_and_build)

        # watch for templates path
        super().watch(f'{self.conf.default_theme_path}/templates/**/*',
                      build)
        if self.conf.theme_path:
            super().watch(f'{self.conf.theme_path}/templates/**/*',
                          build)
        # watch for json agenda path
        super().watch(self.conf.json_agenda_path.as_posix(), build)

        # watch for json team path
        super().watch(self.conf.json_teams_path.as_posix(), build)

        # watch for config path
        super().watch(self.conf.config_path.as_posix(), read_conf_and_build)

        for dirpath in self.conf.static_payload:
            # watch for default payload pathes
            super().watch(
                f"{(self.conf.default_theme_path / dirpath).as_posix()}/**/*",
                website.copy_payload)
            if self.conf.theme_path:
                # watch for user payload pathes
                super().watch(
                    f"{(self.conf.theme_path / dirpath).as_posix()}/**/*",
                    website.copy_payload)
