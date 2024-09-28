from sgelt.data import Data
import datetime


def test_data(miniwebsite):
    data = Data(miniwebsite.conf)
    data.read_files()

    aconf = data.conferences[0]
    assert aconf['date'] == datetime.datetime(2007, 8, 27, 0, 0)
    assert aconf['end'] == datetime.datetime(2007, 8, 27, 0, 0)
    assert aconf['place'] == 'Vincent-sur-Coulon'
    assert aconf['title'] == 'Retourner trois passer calme pleurer si'
    assert data.conferences[0]

    asem = data.seminars[0]
    assert asem['date'] == 'depuis mai 2010'
    assert (asem['full_title'] ==
            'Séminaire Beau souffrance réveiller beauté horizon manquer')
    assert asem['organizer'] == 'Martin-Matthieu Courtois'
    assert asem['status'] == 'actif'
    assert asem['teams'] == ['RA']
    assert asem['title'] == 'Beau souffrance réveiller beauté horizon manquer'
    assert asem['type'] == 'Séminaire'

    adef = data.defenses[0]
    assert adef['type'] == "Soutenance d'HDR"
    assert adef['date'] == datetime.datetime(2004, 3, 3, 2, 1, 15)
    assert adef['place'] == 'Importer'
    assert adef['speaker'] == 'Manon Millet'
    assert adef['title'] == 'Forcer espérer hésiter français travers'
