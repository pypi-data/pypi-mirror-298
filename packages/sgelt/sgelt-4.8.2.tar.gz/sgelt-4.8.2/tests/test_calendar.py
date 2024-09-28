from faker import Faker
from pathlib import Path
import filecmp

from sgelt import calendar


def create_ical_events(n: int) -> list:

    fake = Faker(['fr_FR'])
    Faker.seed(4321)

    ical_events = []
    for _ in range(n):
        dtstart = fake.date_time()
        dend = dtstart + fake.time_delta()
        dtstamp = fake.date_time()
        ical_event = {
            'summary': fake.sentence(),
            'dtstart': dtstart,
            'dtend': dend,
            'dtstamp': dtstamp,
            'uuid': fake.uuid4(),
            'url': fake.url(),
        }
        if fake.boolean(chance_of_getting_true=75):
            ical_event['location'] = fake.sentence(3)[:-1]
        if fake.boolean(chance_of_getting_true=50):
            ical_event['description'] = fake.paragraph(10)
        ical_events.append(ical_event)
    return ical_events


def create_calendar(tmpdir, sem_name=None):

    fake = Faker(['fr_FR'])
    Faker.seed(4321)

    def write_file(filename: str, ical_content: str):
        ical_outpath = tmpdir / Path(filename).with_suffix('.ics')
        ical_outpath.write_text(ical_content, encoding='utf-8')
        return ical_outpath

    if sem_name is None:
        sem_name = fake.name()
    ical_events = create_ical_events(fake.random_int(min=2, max=5))
    ical_content = calendar.build_calendar(
        prodid=f'-//Pilab//Séminaire {sem_name}//FR',
        ical_events=ical_events)
    write_file(sem_name, ical_content)
    return ical_content


def test_build_calendar():

    ical_events = create_ical_events(5)

    s = calendar.build_calendar(prodid="-//Example Corp.//CalDAV Client//EN",
                                ical_events=ical_events)
    assert s == """\
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Example Corp.//CalDAV Client//EN
BEGIN:VEVENT
SUMMARY:Trois passer calme pleurer.
DTSTART;TZID=Europe/Paris;VALUE=DATE-TIME:19870422T043021
DTEND;TZID=Europe/Paris;VALUE=DATE-TIME:19870422T043021
DTSTAMP;VALUE=DATE-TIME:19970924T214947Z
UID:0d9320ac-9626-4f79-af97-3c0cdaaede08
LOCATION:Hiver commencer accompagner
PRIORITY:5
URL:https://marion.net/
END:VEVENT
BEGIN:VEVENT
SUMMARY:Voici paraître cri essuyer patron.
DTSTART;TZID=Europe/Paris;VALUE=DATE-TIME:19800626T111048
DTEND;TZID=Europe/Paris;VALUE=DATE-TIME:19800626T111048
DTSTAMP;VALUE=DATE-TIME:19851210T111856Z
UID:31c51f87-79c5-4148-993a-ea1cd9117f52
DESCRIPTION:Derrière aucun emporter poitrine pont voyager. Sentir égalem
 ent joie mine rapidement saint. En attention rapporter autant moyen force 
 goût maladie. Continuer titre matin révéler bande. Quatre sonner riche 
 glisser sens résultat minute commencer. Drame travailler demain chaise. F
 ermer sûr épais société paysage consulter voler. Cruel aller santé fr
 ançois dimanche parole ce.
LOCATION:Rendre deviner
PRIORITY:5
URL:https://www.lamy.fr/
END:VEVENT
BEGIN:VEVENT
SUMMARY:Envelopper but leur frais accepter.
DTSTART;TZID=Europe/Paris;VALUE=DATE-TIME:19730113T152928
DTEND;TZID=Europe/Paris;VALUE=DATE-TIME:19730113T152928
DTSTAMP;VALUE=DATE-TIME:19850724T050159Z
UID:93f29a6c-ce4c-4636-a1e5-b45a3999b548
DESCRIPTION:Intérieur membre plaisir remonter songer large. Se supporter 
 poche veiller. Auprès sous colère prière enfance protéger lueur. Bas t
 ravailler sortir delà exemple forcer. Durer aventure grandir. Morceau enf
 in portier fermer. Français troisième retrouver ailleurs céder passer. 
 Valeur foi clair expliquer.
LOCATION:Cours peser
PRIORITY:5
URL:http://www.fernandes.com/
END:VEVENT
BEGIN:VEVENT
SUMMARY:Compte croire mal rouler heureux.
DTSTART;TZID=Europe/Paris;VALUE=DATE-TIME:19830425T115619
DTEND;TZID=Europe/Paris;VALUE=DATE-TIME:19830425T115619
DTSTAMP;VALUE=DATE-TIME:20221023T190217Z
UID:e1fa20df-4498-409f-9931-f70c16e26981
DESCRIPTION:Ah simple tourner dos parent. Aujourd'Hui prêter user. Choix 
 sentiment durer reconnaître certain or. Attention soir pleurer droite eh 
 colline beauté. Humide contre dieu. Accorder ici abri toi éclairer muet 
 départ. Entre verre clair éprouver homme. Projet longtemps malgré voie 
 quelque fumée. Lors maison choisir grâce appartement pied coup continuer
 . Inquiéter ou même prouver.
LOCATION:Me retenir
PRIORITY:5
URL:http://www.raymond.fr/
END:VEVENT
BEGIN:VEVENT
SUMMARY:Devoir écouter ombre doute obtenir.
DTSTART;TZID=Europe/Paris;VALUE=DATE-TIME:19920109T230449
DTEND;TZID=Europe/Paris;VALUE=DATE-TIME:19920109T230449
DTSTAMP;VALUE=DATE-TIME:19770918T193738Z
UID:d7683610-8d9b-4489-ac90-a17df9e58981
LOCATION:Au temps
PRIORITY:5
URL:https://gautier.fr/
END:VEVENT
END:VCALENDAR
""".replace('\n', '\r\n')


def test_merge_calendars(tmpdir):

    for _ in range(3):
        create_calendar(tmpdir)

    ics_file_paths = Path(tmpdir).glob('**/*.ics')
    prodid = f'-//Pilab//Séminaires//FR'
    ical_merged = calendar.merge_calendars(prodid, ics_file_paths,
                                           {'Séminaire', 'Colloquium'})
    assert ical_merged.startswith("""\
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Pilab//Séminaires//FR
BEGIN:VEVENT
SUMMARY:Séminaire Antoine-Lucas Andre - Trois passer calme pleurer.
DTSTART;TZID=Europe/Paris;VALUE=DATE-TIME:19870422T043021
DTEND;TZID=Europe/Paris;VALUE=DATE-TIME:19870422T043021
DTSTAMP;VALUE=DATE-TIME:19970924T214947Z
""".replace('\n', '\r\n'))
    assert ical_merged.endswith("""\
DESCRIPTION:Intérieur membre plaisir remonter songer large. Se supporter 
 poche veiller. Auprès sous colère prière enfance protéger lueur. Bas t
 ravailler sortir delà exemple forcer. Durer aventure grandir. Morceau enf
 in portier fermer. Français troisième retrouver ailleurs céder passer. 
 Valeur foi clair expliquer.
LOCATION:Cours peser
PRIORITY:5
URL:http://www.fernandes.com/
END:VEVENT
END:VCALENDAR
""".replace('\n', '\r\n'))


def test_write_calendar_file(tmpdir, miniwebsite):
    sem_name = 'seminaire_test'
    ical_content = create_calendar(tmpdir, sem_name=sem_name)
    ical_url = calendar.write_calendar_file(sem_name, miniwebsite.conf,
                                            ical_content)
    assert ical_url == f"{miniwebsite.conf.site['url']}/cal/{sem_name}.ics"
    assert filecmp.cmp(
        f"{tmpdir}/{sem_name}.ics",
        miniwebsite.conf.output_path / "cal" / f"{sem_name}.ics")


def test_SeminarTopIndexPage(miniwebsite):
    miniwebsite.build()
    ical_filepath = Path('cal/seminaires.ics')
    ical_outpath = miniwebsite.conf.output_path / ical_filepath
    ical_content = ical_outpath.read_text()
    assert ical_content.startswith("""\
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Pilab//séminaires//FR
BEGIN:VEVENT
SUMMARY:Séminaire Beau souffrance réveiller beauté horizon manquer - Lu
 cie Daniel - Admettre propre existence crainte mot prochain bas
DTSTART;TZID=Europe/Paris;VALUE=DATE-TIME:20180625T042207
""")
    assert ical_content.endswith("""\
DESCRIPTION:Saint extraordinaire pur couler exiger vif retour anglais. Noi
 r autrement papa rapidement. Raison près arbre en révéler phrase. Air d
 éjà droit verser offrir. Aucun condition exiger nouveau grand disparaît
 re terrain eau. Brûler étendre quarante pain. Bon fait blanc rire sortir
  douze. L'Une terreur religion contenir. Direction depuis respecter créer
 . Courir et durant. Abri huit reprendre reculer chiffre.
LOCATION:salle de troubler
PRIORITY:5
URL:https://fakelab.fk/seminaires/seminaire-donc-repas-eternel-sein-traver
 s-penetrer.html
END:VEVENT
END:VCALENDAR
""")
