from multiprocessing import Process

from sgelt import watch


def test_watch(miniwebsite):
    conf = miniwebsite.conf
    p = Process(target=watch.watch, args=(conf,))
    try:
        p.start()
        conf.config_path.touch()
    finally:
        p.join(timeout=3)
        if p.is_alive():
            p.terminate()
