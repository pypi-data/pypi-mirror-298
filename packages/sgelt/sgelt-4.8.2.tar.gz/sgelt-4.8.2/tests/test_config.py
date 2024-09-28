from pathlib import Path
from datetime import datetime

from common import test_path, freeze_today
from sgelt import config, package_dir


def test_conf():

    conf = config.Config()

    s = f"""\
args: None
default_theme_path: {package_dir.as_posix()}/theme
theme_path: None
output_path: output
content_path: content
config_path: config.yml
static_payload:
    - css
    - js
    - img
json_agenda_path: agenda_mysql.json
json_teams_path: teams.json
search_index: True
templates_paths:
    - {package_dir.as_posix()}/theme/templates
site: None\
"""
    # Check default conf
    assert str(conf) == s

    # Test conf update

    # theme dir does not exist so do not update
    conf.update(theme_path=test_path/"theme/nothing")
    assert conf.theme_path == test_path / "theme/nothing"
    assert conf.templates_paths == [package_dir / 'theme/templates']

    # theme dir does exist so do update
    conf.update(theme_path=test_path/"theme/test")
    assert conf.theme_path == test_path / "theme/test"
    assert conf.templates_paths == [package_dir / 'theme/templates',
                                    test_path / "theme/test/templates"]

    conf.update(static_payload=('style', ))
    assert conf.static_payload == [Path("style"), ]
    conf.update(json_agenda_path=test_path / 'fake_agenda.json')
    assert conf.json_agenda_path == test_path / 'fake_agenda.json'
    config_path = test_path / 'config.yml'
    conf.update(config_path=config_path)
    assert conf.config_path == config_path

    # Test read config.yml and load data
    conf.load()
    assert conf.theme_path == Path("theme/test")
    assert conf.templates_paths == [package_dir / 'theme/templates',
                                    test_path / "theme/test/templates"]
    conf.update(content_path='spam')
    assert conf.site['homepage']['title'] == '&Pi; Lab'
    assert conf.site['homepage']['carroussel_max'] == 5
    assert (conf.site['nav_items']["Le laboratoire"]
            ['Présentation'] == "lelaboratoire/presentation.html")
    assert conf.site['today'] == datetime.strptime(freeze_today,
                                                   '%Y-%m-%d').date()


def test_conf_with_cli_args():

    class CLIArgs:
        """A mockup class for CLI arguments"""

        theme_path = 'path/to/theme'
        output = 'path/to/output'
        content = 'path/to/content'
        json_agenda = 'path/to/agenda_mysql.json'
        json_teams = 'path/to/teams.json'
        search_index = False

    config_path = test_path / 'config.yml'
    conf = config.Config(config_path=config_path, args=CLIArgs())
    conf.load()
    s = f"""\
default_theme_path: {package_dir.as_posix()}/theme
theme_path: theme/test
output_path: path/to/output
content_path: path/to/content
config_path: {config_path}
static_payload:
    - css
    - js
    - img
json_agenda_path: path/to/agenda_mysql.json
json_teams_path: path/to/teams.json
search_index: False
templates_paths:
    - {package_dir.as_posix()}/theme/templates
    - {test_path.as_posix()}/theme/test/templates
"""
    assert s in str(conf)


def test_conf_with_config_path():

    conf = config.Config(config_path=test_path / 'config.yml')
    conf.load()
    s = f"""\
args: None
default_theme_path: {package_dir.as_posix()}/theme
theme_path: theme/test
output_path: output
content_path: content
config_path: {test_path.as_posix()}/config.yml
static_payload:
    - css
    - js
    - img
json_agenda_path: fake_agenda.json
json_teams_path: fake_teams.json
search_index: True
templates_paths:
    - {package_dir.as_posix()}/theme/templates
    - {test_path.as_posix()}/theme/test/templates
"""
    assert s == str(conf).split('site:\n')[0]
