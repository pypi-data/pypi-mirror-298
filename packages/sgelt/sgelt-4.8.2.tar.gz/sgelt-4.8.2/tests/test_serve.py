import pytest
from sgelt import serve
from multiprocessing import Process


@pytest.fixture
def server(miniwebsite):
    server = serve.MyServer(miniwebsite.conf)
    return server


def run_process(p: Process, timeout: int):
    """Run and terminate process"""
    try:
        p.start()
    finally:
        # necessary so that the Process exists before the test suite exits
        # (thus coverage is collected)
        p.join(timeout=timeout)
        if p.is_alive():
            p.terminate()


def test_serve(server):
    p = Process(target=server.serve, args=(False,))
    run_process(p, timeout=1)


def test_serve_browser(server):
    p = Process(target=server.serve, args=(True,))
    run_process(p, timeout=1)


def test_watch_config(server):
    p = Process(target=server.watch)
    try:
        p.start()
        server.conf.config_path.touch()
    finally:
        p.join(timeout=2)
        if p.is_alive():
            p.terminate()


def test_serve_random_port(server):

    p = Process(target=server.serve, args=(False,))
    p2 = Process(target=server.serve, args=(False,))
    try:
        p.start()
        p2.start()
    finally:
        p.join(timeout=1)
        p2.join(timeout=1)
        if p.is_alive():
            p.terminate()
        if p2.is_alive():
            p2.terminate()


def test_watch(server):

    p = Process(target=server.watch)
    run_process(p, timeout=2)
