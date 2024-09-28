import pytest
from sgelt import serve


@pytest.fixture
def server(miniwebsite):
    server = serve.MyServer(miniwebsite.conf)
    return server


def test_watch(miniwebsite):
    server = serve.MyServer(miniwebsite.conf)
    server.watch()
    server.conf.config_path.touch()
