import os
import pytest
import argparse
from pathlib import PosixPath
import signal
from contextlib import redirect_stdout
import io
import platform

from sgelt import main, __version__


@pytest.fixture(scope="function", autouse=True)
def change_test_dir(request):
    os.chdir(request.fspath.dirname)
    yield
    os.chdir(request.config.invocation_dir)


@pytest.fixture
def output_path(tmp_path):
    return tmp_path / "output"


def test_parser():
    # Default
    parser = main.parse_args([])

    assert parser == argparse.Namespace(
        debug=False, config=PosixPath('config.yml'), json_agenda=None,
        json_teams=None, content=None, output=None,
        search_index=True, serve=False, browser=False, auto=False, reset=False,
        version=False)
    parser = main.parse_args(['--debug'])
    assert parser.debug is True
    parser = main.parse_args(['--config', 'spam.yml'])
    assert parser.config == 'spam.yml'
    parser = main.parse_args(['--json_agenda', 'egg.json'])
    assert parser.json_agenda == 'egg.json'
    parser = main.parse_args(['--json_teams', 'tomatoes.json'])
    assert parser.json_teams == 'tomatoes.json'
    parser = main.parse_args(['--content', 'bacon'])
    assert parser.content == 'bacon'
    parser = main.parse_args(['--output', 'spam/bacon'])
    assert parser.output == 'spam/bacon'
    parser = main.parse_args(['--noindex'])
    assert parser.search_index is False

    # watcher
    parser = main.parse_args(['--serve'])
    assert parser.serve is True
    parser = main.parse_args(['--browser'])
    assert parser.browser is True
    parser = main.parse_args(['--auto'])
    assert parser.auto is True

    # cleaner
    parser = main.parse_args(['--reset'])
    assert parser.reset is True

    # version
    parser = main.parse_args(['--version'])
    assert parser.version is True


def timeout_handler(*args):
    raise Exception("Controlled timeout")


signal.signal(signal.SIGALRM, timeout_handler)


def test_main_output(mocker, output_path):

    mocker.patch("sys.argv", ['sgelt', '-o', output_path.as_posix()])
    main.main()
    assert (output_path / "lunr_content.js").exists()

    mocker.patch("sys.argv",
                 ['sgelt', '--noindex', '-o', output_path.as_posix()])
    main.main()
    assert not (output_path / "lunr_content.js").exists()


def test_main_serve(mocker):
    mocker.patch("sys.argv", ['sgelt', '-s'])
    signal.setitimer(signal.ITIMER_REAL, 0.1)
    try:
        main.main()
    except Exception as e:
        assert str(e) == "Controlled timeout"
    finally:
        signal.alarm(0)


def test_main_browser_alone(mocker):
    mocker.patch("sys.argv", ['sgelt', '-b'])
    try:
        main.main()
    except SystemExit as e:
        assert e.code == '-b/--browser cannot be used without -s/--serve'
    else:
        assert False


def test_main_serve_browser(mocker):
    mocker.patch("sys.argv", ['sgelt', '-b', '-s'])
    signal.setitimer(signal.ITIMER_REAL, 0.1)
    try:
        main.main()
    except Exception as e:
        assert str(e) == "Controlled timeout"
    finally:
        signal.alarm(0)


@pytest.mark.skipif(platform.system() == 'Linux',
                    reason="Watchdog does not work correctly on Linux")
def test_main_auto_alone(mocker, output_path):
    mocker.patch("sys.argv", ['sgelt', '-a', '-o', output_path.as_posix()])
    signal.setitimer(signal.ITIMER_REAL, 0.5)
    try:
        main.main()
    except Exception as e:
        assert str(e) == "Controlled timeout"
    finally:
        signal.alarm(0)


def test_main_auto_with_server(mocker, output_path):
    mocker.patch("sys.argv",
                 ['sgelt', '-a', '-s', '-o', output_path.as_posix()])
    signal.setitimer(signal.ITIMER_REAL, 1)
    try:
        main.main()
    except Exception as e:
        assert str(e) in ("Controlled timeout",
                          "[Errno 98] Address already in use")
    finally:
        signal.alarm(0)


def test_main_version(mocker):
    mocker.patch("sys.argv", ['sgelt', '-v'])
    # Get stdout
    f = io.StringIO()
    with redirect_stdout(f):
        main.main()
    s = f.getvalue()
    assert s == f'Sgelt {__version__}\n'


def test_main_reset(mocker, output_path):
    mocker.patch("sys.argv", ['sgelt', '-o', output_path.as_posix()])
    main.main()
    assert output_path.exists()
    assert output_path.is_dir()
    mocker.patch("sys.argv", ['sgelt', '-r', '-o', output_path.as_posix()])
    main.main()
    assert not output_path.exists()
