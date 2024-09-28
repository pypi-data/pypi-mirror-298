"""Define site configuration class and instantiate in a conf object"""

from datetime import date, datetime
import jinja2
import logging
from pathlib import Path
import yaml

from . import filters, package_dir, __version__

log = logging.getLogger(__name__)


class Config:
    """A class to store site configuration"""

    # Default config dict that may be overriden by user values
    def_conf = dict(
        default_theme_path=package_dir / 'theme',
        theme_path=None,
        output_path='output',
        content_path='content',
        config_path='config.yml',
        static_payload=('css', 'js', 'img'),
        json_agenda_path='agenda_mysql.json',
        json_teams_path='teams.json',
        search_index=True
    )

    def __init__(self, args=None, config_path=None):
        """Set class attributes from default"""
        self.args = args
        conf = self.def_conf.copy()
        self._set_attributes(conf)
        # Update config.yml default path
        if config_path is not None:
            self.update(config_path=config_path)
        else:
            try:
                self.update(config_path=self.args.config_path)
            except AttributeError:
                pass
        self.site = None

    def save_args(self) -> dict:
        """Return a dict of config.__init__() arguments"""
        return {'args': self.args, 'config_path': self.config_path}

    def update(self, **kwargs):
        """Update object attributes from names args"""
        conf = vars(self)  # get attributes as dict
        # Update conf dict with init args if key exists
        for k, v in kwargs.items():
            if k in self.def_conf:
                conf[k] = v
            else:
                log.warning(f"Cannot update conf dict with unknown key: {k}")
        self._set_attributes(conf)

    def load(self):
        """Parse YAML config file and override with CLI args"""

        # Read config.yml file
        try:
            with open(self.config_path) as f:
                file_conf = yaml.safe_load(f)
        except FileNotFoundError as e:
            log.error(e)
            log.debug(self)
            import sys
            sys.exit(1)

        # site dict becomes .site attribute
        self.site = file_conf.pop('site')

        # Convert path/to/file.md -> path/to/file.html
        for dropdown_items in self.site['nav_items'].values():
            try:
                for dropdown_name, filename in dropdown_items.items():
                    filepath = Path(filename)
                    # Convert markdown paths to html paths
                    if filepath.suffix == '.md':
                        dropdown_items[dropdown_name] = filepath.with_suffix(
                            '.html').as_posix()
            except AttributeError:
                # dropdown_items is not an actual dropdown dict
                pass

        if 'today' in self.site:
            # Convert today as date if exists
            if type(self.site['today']) is not date:
                self.site['today'] = self.site['today'].date()
        else:
            # Use today date
            self.site['today'] = date.today()

        # update other attributes (same as in def_conf)
        self.update(**file_conf)

        # Override with CLI args
        args = self.args
        if args is not None:
            if args.json_agenda:
                self.update(json_agenda_path=args.json_agenda)
            if args.json_teams:
                self.update(json_teams_path=args.json_teams)
            if args.content:
                self.update(content_path=args.content)
            if args.output:
                self.update(output_path=args.output)
            if not args.search_index:
                self.update(search_index=False)

    def _set_attributes(self, conf: dict):
        """From conf dict and default values, set class attributes"""
        for k, v in conf.items():
            if k != 'env':
                if isinstance(v, list) or isinstance(v, tuple):
                    setattr(self, k, [Path(item) for item in v])
                elif isinstance(v, dict) or isinstance(v, type(None)):
                    setattr(self, k, v)
                elif isinstance(v, type(None)):
                    pass
                else:
                    try:
                        setattr(self, k, Path(v))
                    except TypeError:
                        setattr(self, k, v)

        self.templates_paths = [self.default_theme_path / Path('templates')]
        try:
            if conf['theme_path'] and conf['theme_path'].is_relative_to(
                    self.config_path.parent):
                conf_theme_path = conf['theme_path']
            else:
                conf_theme_path = self.config_path.parent / conf['theme_path']
            user_template_path = conf_theme_path / 'templates'
            if user_template_path.exists():  # Add override template dir
                self.templates_paths.append(user_template_path)
        except TypeError:  # self.theme_path is None thus skip
            pass
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.templates_paths)
        )

        # Add filters
        self.env.filters['homepage'] = filters.homepage
        self.env.filters['agenda'] = filters.agenda
        self.env.filters['event_date_time'] = filters.event_date_time
        self.env.filters['categ_to_target'] = filters.categ_to_target
        self.env.filters['url'] = filters.url
        self.env.filters['external_url'] = filters.external_url
        self.env.filters['event_selector'] = filters.event_selector
        self.env.filters['sort_by_date'] = filters.sort_by_date
        self.env.filters['homepage_news'] = filters.homepage_news
        self.env.filters['news_page'] = filters.news_page
        self.env.filters['dropdown_items'] = filters.dropdown_items
        self.env.filters['real_teams'] = filters.real_teams
        self.env.filters['teams'] = filters.teams
        self.env.filters['organizing_teams'] = filters.organizing_teams

        # Global variables
        self.env.globals['datetime_min'] = datetime.min
        self.env.globals['sgelt_version'] = __version__

    def __repr__(self):
        def _format(k, v):
            if isinstance(v, list):
                return "{}:\n{}".format(k, '\n'.join((f"    - {item}"
                                                      for item in v)))
            elif isinstance(v, dict):
                import textwrap
                return f"""\
{k}:\n{textwrap.indent(yaml.dump(v, allow_unicode=True), 2 * ' ')}"""
            else:
                return f"{k}: {v}"
        return '\n'.join((_format(k, v)
                          for k, v in vars(self).items()
                          if not isinstance(v, jinja2.Environment)))
