import filecmp
import datetime
import os
from pathlib import Path
import pytest


from common import test_path, test_abstract
from sgelt import utils


def test_copy_file(tmp_path):
    src_dir = tmp_path / "src/subdir1/subdir2"
    os.makedirs(src_dir)
    src = src_dir / 'spam.txt'
    src.write_text("egg")
    dst_dir = tmp_path / "dst/subdir1/subdir2"
    dst = dst_dir / 'spam.txt'
    utils.copy_file(src, dst)
    # Ensure content is identical
    assert filecmp.cmp(src, dst, shallow=False)

    # Source and destination are identical so do not copy
    m_time_src = src.stat().st_mtime
    utils.copy_file(src, dst)
    assert src.stat().st_mtime == m_time_src

    # Files are different so copy
    src.write_text("bacon")
    assert not filecmp.cmp(src, dst)
    utils.copy_file(src, dst)
    assert filecmp.cmp(src, dst, shallow=False)

    # File does not exist
    src = tmp_path / 'tomatoes'
    dst = tmp_path / 'spam/tomatoes'
    utils.copy_file(src, dst)
    assert dst.is_file() is False


def test_read_data():
    data = utils.read_data(test_path / 'fake_agenda.json')
    expected_time_slot = {
        'affiliation': 'Devaux Rocher et Fils',
        'date': datetime.datetime(2007, 8, 27, 8, 0),
        'end': None,
        'speaker': 'Martin Georges',
        'start': datetime.datetime(2007, 8, 27, 8, 0),
        'title': 'Retenir cours peser autant.',
        'type': 'Communication',
        'abstract': test_abstract
    }
    # from pprint import pprint
    # pprint(data['conferences'][0]['program'])
    found_time_slot = data['conferences'][0]['program']['2007-08-27 00:00:00']['time_slots'][0]
    assert expected_time_slot == found_time_slot


def test_MetaDataParsingError(tmp_path):
    md_filepath = tmp_path / "test.md"
    metadata = {'title': 'Présentation',
                'menu_item': "L'institut",
                'category': "static",
                'date': '2015-02-03 15:28'}
    with pytest.raises(utils.MetaDataParsingError) as e:
        raise utils.MetaDataParsingError(md_filepath, metadata)
    assert '2015-02-03 15:28' in str(e.value)


def test_parse_md_file(tmp_path):
    template = """\
---
title: Présentation
menu_item: "L'institut"
category: "static"
date: {}
---

Some content on
two lines.

"""

    def get_expected_template(date_obj) -> dict:
        return {'title': "Présentation",
                'menu_item': "L'institut",
                'category': "static",
                'date': date_obj}

    s = template.format('2015-02-03 15:28:09')
    # Write string content in test.md
    md_filepath = tmp_path / "test.md"
    md_filepath.write_text(s)

    metadata, md_content = utils.parse_md_file(md_filepath)
    assert metadata == get_expected_template(
        datetime.datetime(2015, 2, 3, 15, 28, 9))
    assert md_content == 'Some content on\ntwo lines.'

    s = template.format('2015-02-03')

    # Write string content in test.md
    md_filepath = tmp_path / "test.md"
    md_filepath.write_text(s)

    metadata, md_content = utils.parse_md_file(md_filepath)
    assert metadata == get_expected_template(datetime.date(2015, 2, 3))
    assert md_content == 'Some content on\ntwo lines.'

    s = template.format('2015-02-03 15:28')
    # Write string content in test.md
    md_filepath = tmp_path / "test.md"
    md_filepath.write_text(s)
    with pytest.raises(SystemExit) as e:
        utils.parse_md_file(md_filepath)
    assert e.type == SystemExit
    assert e.value.code == 1


def test_override_default():

    payload_paths = []
    default_basepath = test_path / 'diff/left/'
    override_basepath = test_path / 'diff/right/'
    dcmp = filecmp.dircmp(default_basepath, override_basepath)
    utils.override_default(payload_paths, dcmp)

    expected_files = ('diff/left/js/a.js',
                      'diff/right/css/a.css',
                      'diff/right/img/c.jpg',
                      'diff/right/img/a.jpg',
                      'diff/right/img/b.jpg')
    expected = set(test_path / path for path in expected_files)
    assert set(payload_paths) == expected


def test_clean_project(tmp_path):
    project_dir = tmp_path / 'project'
    os.makedirs(project_dir)
    utils.clean_project(project_dir)
    assert project_dir.is_dir() is False
    # FileNotFoundError
    utils.clean_project(project_dir)


def test_get_socket_port():
    port = utils.get_socket_port()
    # port number depends on currently open sockets on the system
    assert port >= 5500


common_samples = (
    ('this is a test', 'this-is-a-test'),
    ('this        is a test', 'this-is-a-test'),
    ('this → is ← a ↑ test', 'this-is-a-test'),
    ('this--is---a test', 'this-is-a-test'),
    ('Hello World', 'hello-world'),
    ("A / should be replaced", "a-should-be-replaced"),
    ("No , are tolerated", "no-are-tolerated"))


def test_slugify():
    specific_samples = (
        ('unicode測試許功蓋，你看到了嗎？',
         'unicodece-shi-xu-gong-gai-ni-kan-dao-liao-ma'),
        ('大飯原発４号機、１８日夜起動へ',
         'da-fan-yuan-fa-4hao-ji-18ri-ye-qi-dong-he'),
        ("Coucou l'ami", "coucou-l-ami"),
        ("replace:from/filepath/but/keep/dot.html",
         "replace:from-filepath-but-keep-dot.html"),)

    for value, expected in common_samples + specific_samples:
        assert utils.slugify(value) == expected


def test_md_slugify():
    specific_samples = (
        ('unicode測試許功蓋，你看到了嗎？',
         'unicode'),
        ('大飯原発４号機、１８日夜起動へ', '418'),
        ("Coucou l'ami", "coucou-lami"),
        ("remove:from/filepath.html",
         "removefromfilepathhtml"),)

    for value, expected in common_samples + specific_samples:
        assert utils.md_slugify(value) == expected


def test_slugify_path():
    samples = (
        ("Groupe de travail/groupe de travail détection d'anomalies.html",
         "groupe-de-travail/groupe-de-travail-detection-d-anomalies.html"),
        ("séminaire/groupe de travail détection d'anomalies.html",
         "seminaire/groupe-de-travail-detection-d-anomalies.html"),)
    for value, expected in samples:
        assert utils.slugify_path(Path(value)) == Path(expected)


def test_get_short_uid():
    uids = [utils.get_short_uid() for _ in range(100)]
    # Check that uids are uniques
    assert len(uids) == len(set(uids))
    # Check that uids are 6-digit
    for uid in uids:
        assert len(str(uid)) == 6
