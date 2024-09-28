from sgelt.pages import (
    Paginator,
    Page, MdPage, ConferencePage, DefensePage, SeminarPage,
    SeminarTopIndexPage, WorkGroupTopIndexPage, IndexPage, NewsPage,
    VirtualNewsPage, LibNewsPage, NewsIndexPage, LibNewsIndexPage, HomePage,
    mdparse)
from sgelt.sgelt import Website
from sgelt import utils
from pathlib import Path
import os
import datetime
from common import test_content_path


def test_paginator():
    names = ["à venir", 2020, 2019, 2017]
    p = Paginator(names, "test.html")

    assert p.get_filename("à venir") == "test.html"
    assert p.has_next("à venir")
    assert not p.has_previous("à venir")
    assert p.previous_filename("à venir") == "#"
    assert p.next_filename("à venir") == "test-2020.html"

    assert p.get_filename(2017) == "test-2017.html"
    assert not p.has_next(2017)
    assert p.has_previous(2017)
    assert p.previous_filename(2017) == "test-2019.html"
    assert p.next_filename(2017) == "#"

    assert p.previous_filename(2020) == "test.html"
    assert p.previous_filename(2019) == "test-2020.html"
    assert p.next_filename(2019) == "test-2017.html"


def test_MdPage(miniwebsite, tmp_path):
    s = """
---
title: Présentation
menu_item: "L'institut"
category: "static"
date: 2015-02-03 15:28:09
---

## Présentation

![Tour IRMA](img/tour_irma.jpg){: .materialboxed .responsive-img }

Riche d’une histoire de plus de 100 ans, l’IRMA est depuis 1997 une unité mixte de recherche (UMR 7501).

## Histoire

Fondé il y a plus de cent ans, l’IRMA a été marqué par une succession de mathématiciens de renom comme Heinrich Weber.
"""
    conf = miniwebsite.conf
    # Initialize output path
    conf.update(content_path=tmp_path / "content")
    conf.output_path.mkdir()

    # Write string content in test.md
    conf.content_path.mkdir()
    md_filepath = conf.content_path / "subdir1/subdir2/test.md"
    os.makedirs(md_filepath.parent, exist_ok=True)
    md_filepath.write_text(s)
    metadata, md_content = utils.parse_md_file(md_filepath)
    page = MdPage(miniwebsite, md_filepath, metadata, md_content)
    assert page.title == "Présentation"
    assert page.menu_item == "L'institut"
    assert page.category == "static"
    assert page.metadata == {'title': "Présentation",
                             'menu_item': "L'institut",
                             'category': "static",
                             'date': datetime.datetime(2015, 2, 3, 15, 28, 9)}
    assert conf.output_path / page.html_path == (
        tmp_path / Path("output/subdir1/subdir2/test.html"))
    assert page.template_path == Path("article.html")

    sections, toc = mdparse.get_sections(page.md_content)
    assert toc == [
        {'level': 2, 'id': 'presentation', 'name': 'Présentation', 'html': 'Présentation', 'data-toc-label': '',
         'children': []},
        {'level': 2, 'id': 'histoire', 'name': 'Histoire', 'html': 'Histoire', 'data-toc-label': '', 'children': []}
    ]

    section_1_content = """
<p><img alt="Tour IRMA" class="materialboxed responsive-img" src="img/tour_irma.jpg"/></p>
<p>Riche d’une histoire de plus de 100 ans, l’IRMA est depuis 1997 une unité mixte de recherche (UMR 7501).</p>
"""
    section_2_content = """
<p>Fondé il y a plus de cent ans, l’IRMA a été marqué par une succession de mathématiciens de renom comme Heinrich Weber.</p>\
"""
    assert sections == [{'title': 'Présentation', 'id': 'presentation', 
                         'content': section_1_content},
                        {'title': 'Histoire', 'id': 'histoire',
                         'content': section_2_content}]
    # Test if render do not fail
    page.render()
    assert (conf.output_path / page.html_path).is_file()

    # Test json node for lunr.js
    assert page.get_index_node() == {
        'tags': ['static'],
        'text': "Présentation - Riche d'une histoire de plus de 100 ans, l'IRMA est "
        'depuis 1997 une unité mixte de recherche (UMR 7501). Histoire - '
        "Fondé il y a plus de cent ans, l'IRMA a été marqué par une "
        'succession de mathématiciens de renom comme Heinrich Weber.',
        'title': 'Présentation',
        'url': 'subdir1/subdir2/test.html',
        'date': '03/02/2015'
    }

    # Test for test content/ dir
    website = Website(conf)
    for page in website.md_pages():
        page.render()


def test_Page(miniwebsite, tmpdir):

    page = Page(miniwebsite, 'index.html', None)
    page.render()
    filepath = Path('index.html')
    assert page.filepath == filepath
    assert page.template_path == filepath
    assert page.html_path == filepath
    assert page.out_path.as_posix().endswith('/output/index.html')

    page = Page(miniwebsite, 'search.html', 'Search')
    page.render()
    filepath = Path('search.html')
    assert page.filepath == filepath
    assert page.menu_item == "Search"
    assert page.template_path == filepath
    assert page.html_path == filepath
    assert page.out_path.as_posix().endswith('/output/search.html')
    assert str(page) == f"""
Page:
  title: ''
  category: ''
  filepath: PosixPath('search.html')
  template_name: ''
  template_path: PosixPath('search.html')
  menu_item: 'Search'
  virtual: False
  html_path: PosixPath('search.html')
  out_path: PosixPath('{tmpdir}/output/search.html')
  content: ''
"""


def test_ConferencePage(miniwebsite):

    conference = miniwebsite.data.conferences[0]
    page = ConferencePage(miniwebsite,
                          menu_item="Agenda",
                          title=conference['title'],
                          template_name="conference.html",
                          category='conférence',
                          event=conference)

    page.render()
    # the ref dictionany is obtained using:
    # from pprint import pprint
    # pprint(page.get_index_node())
    assert page.get_index_node() == {
        'date': '27/08/2007',
        'tags': ['conférence'],
        'text': 'Dégager personne santé hiver commencer accompagner manquer haut. '
        'Voici paraître cri essuyer patron. Jamais effacer sorte être flot '
        'aussi espoir ouvrage. Derrière aucun emporter poitrine pont voyager. '
        'Sentir également joie mine rapidement saint. Martin Georges - '
        "Retenir cours peser autant. - Euler's formula, named after Leonhard "
        'Euler, is a mathematical formula in complex analysis that '
        'establishes the fundamental relationship between the trigonometric '
        "functions and the complex exponential function. Euler's formula "
        'states that for any real number $x$: $$e&#94;{ix} = \\cos x + i\\sin '
        'x,$$ where $e$ is the base of the natural logarithm, $i$ is the '
        'imaginary unit, and $\\cos$ and $\\sin$ are the trigonometric '
        'functions cosine and sine respectively. This complex exponential '
        'function is sometimes denoted cis $x$ ("cosine plus i sine"). The '
        'formula is still valid if $x$ is a complex number, and so some '
        "authors refer to the more general complex version as Euler's "
        "formula. Euler's formula is ubiquitous in mathematics, physics, and "
        'engineering. The physicist Richard Feynman called the equation "our '
        'jewel" and "the most remarkable formula in mathematics". When $x = '
        "\\pi$, Euler's formula may be rewritten as $e&#94;{i\\pi} + 1 = 0$, "
        "which is known as Euler's identity. Antoinette de la Devaux - Bas "
        "véritable se supporter poche veiller renoncer. - Euler's formula, "
        'named after Leonhard Euler, is a mathematical formula in complex '
        'analysis that establishes the fundamental relationship between the '
        'trigonometric functions and the complex exponential function. '
        "Euler's formula states that for any real number $x$: $$e&#94;{ix} = "
        '\\cos x + i\\sin x,$$ where $e$ is the base of the natural '
        'logarithm, $i$ is the imaginary unit, and $\\cos$ and $\\sin$ are '
        'the trigonometric functions cosine and sine respectively. This '
        'complex exponential function is sometimes denoted cis $x$ ("cosine '
        'plus i sine"). The formula is still valid if $x$ is a complex '
        'number, and so some authors refer to the more general complex '
        "version as Euler's formula. Euler's formula is ubiquitous in "
        'mathematics, physics, and engineering. The physicist Richard Feynman '
        'called the equation "our jewel" and "the most remarkable formula in '
        'mathematics". When $x = \\pi$, Euler\'s formula may be rewritten as '
        "$e&#94;{i\\pi} + 1 = 0$, which is known as Euler's identity. Guy Le "
        "Gall - Bonheur bas travailler sortir delà exemple forcer. - Euler's "
        'formula, named after Leonhard Euler, is a mathematical formula in '
        'complex analysis that establishes the fundamental relationship '
        'between the trigonometric functions and the complex exponential '
        "function. Euler's formula states that for any real number $x$: "
        '$$e&#94;{ix} = \\cos x + i\\sin x,$$ where $e$ is the base of the '
        'natural logarithm, $i$ is the imaginary unit, and $\\cos$ and '
        '$\\sin$ are the trigonometric functions cosine and sine '
        'respectively. This complex exponential function is sometimes denoted '
        'cis $x$ ("cosine plus i sine"). The formula is still valid if $x$ is '
        'a complex number, and so some authors refer to the more general '
        "complex version as Euler's formula. Euler's formula is ubiquitous in "
        'mathematics, physics, and engineering. The physicist Richard Feynman '
        'called the equation "our jewel" and "the most remarkable formula in '
        'mathematics". When $x = \\pi$, Euler\'s formula may be rewritten as '
        "$e&#94;{i\\pi} + 1 = 0$, which is known as Euler's identity. Georges "
        "Simon - Obliger seuil soulever demain soir toi français. - Euler's "
        'formula, named after Leonhard Euler, is a mathematical formula in '
        'complex analysis that establishes the fundamental relationship '
        'between the trigonometric functions and the complex exponential '
        "function. Euler's formula states that for any real number $x$: "
        '$$e&#94;{ix} = \\cos x + i\\sin x,$$ where $e$ is the base of the '
        'natural logarithm, $i$ is the imaginary unit, and $\\cos$ and '
        '$\\sin$ are the trigonometric functions cosine and sine '
        'respectively. This complex exponential function is sometimes denoted '
        'cis $x$ ("cosine plus i sine"). The formula is still valid if $x$ is '
        'a complex number, and so some authors refer to the more general '
        "complex version as Euler's formula. Euler's formula is ubiquitous in "
        'mathematics, physics, and engineering. The physicist Richard Feynman '
        'called the equation "our jewel" and "the most remarkable formula in '
        'mathematics". When $x = \\pi$, Euler\'s formula may be rewritten as '
        "$e&#94;{i\\pi} + 1 = 0$, which is known as Euler's identity. Michel "
        "Le Colin - Foi clair expliquer. - Euler's formula, named after "
        'Leonhard Euler, is a mathematical formula in complex analysis that '
        'establishes the fundamental relationship between the trigonometric '
        "functions and the complex exponential function. Euler's formula "
        'states that for any real number $x$: $$e&#94;{ix} = \\cos x + i\\sin '
        'x,$$ where $e$ is the base of the natural logarithm, $i$ is the '
        'imaginary unit, and $\\cos$ and $\\sin$ are the trigonometric '
        'functions cosine and sine respectively. This complex exponential '
        'function is sometimes denoted cis $x$ ("cosine plus i sine"). The '
        'formula is still valid if $x$ is a complex number, and so some '
        "authors refer to the more general complex version as Euler's "
        "formula. Euler's formula is ubiquitous in mathematics, physics, and "
        'engineering. The physicist Richard Feynman called the equation "our '
        'jewel" and "the most remarkable formula in mathematics". When $x = '
        "\\pi$, Euler's formula may be rewritten as $e&#94;{i\\pi} + 1 = 0$, "
        "which is known as Euler's identity. Alexandrie-Sophie Hubert - "
        "Heureux beau distance sérieux précipiter tracer. - Euler's formula, "
        'named after Leonhard Euler, is a mathematical formula in complex '
        'analysis that establishes the fundamental relationship between the '
        'trigonometric functions and the complex exponential function. '
        "Euler's formula states that for any real number $x$: $$e&#94;{ix} = "
        '\\cos x + i\\sin x,$$ where $e$ is the base of the natural '
        'logarithm, $i$ is the imaginary unit, and $\\cos$ and $\\sin$ are '
        'the trigonometric functions cosine and sine respectively. This '
        'complex exponential function is sometimes denoted cis $x$ ("cosine '
        'plus i sine"). The formula is still valid if $x$ is a complex '
        'number, and so some authors refer to the more general complex '
        "version as Euler's formula. Euler's formula is ubiquitous in "
        'mathematics, physics, and engineering. The physicist Richard Feynman '
        'called the equation "our jewel" and "the most remarkable formula in '
        'mathematics". When $x = \\pi$, Euler\'s formula may be rewritten as '
        "$e&#94;{i\\pi} + 1 = 0$, which is known as Euler's identity.",
        'title': 'Retourner trois passer calme pleurer si',
        'url': 'conferences/retourner-trois-passer-calme-pleurer-si-4764.html'
    }


def test_DefensePage(miniwebsite):

    defense = miniwebsite.data.defenses[0]
    page = DefensePage(miniwebsite,
                       menu_item="Agenda",
                       title=defense['title'],
                       template_name="soutenance.html",
                       category='soutenance',
                       event=defense)
    page.render()
    # the ref dictionany is obtained using:
    # from pprint import pprint
    # pprint(page.get_index_node())
    assert page.get_index_node() == {
        'date': '03/03/2004',
        'tags': ['soutenance'],
        'text': 'Tandis Que faveur confondre approcher former. Note matin cinq beaux '
        'habiller gros longtemps preuve. Pousser alors condamner produire. '
        'Jaune sauter grâce tout examiner. Verser rue oncle élément idée '
        'silencieux écarter dur. Bord taille peine effort pour sauter debout '
        'chemin. Mentir surprendre seuil départ hôtel. Beaux eh son situation '
        'respirer souffrir armer lors. Composer nerveux public reprendre. '
        'Planche nu âme répéter. Mari bouche même roi. Pourquoi consentir '
        'beau dégager mémoire admettre. Larme effet refuser bras sentiment. '
        'Précipiter sol etc an occuper sans en. Soirée durer être souvent '
        'souvenir chaise chant. Manon Millet',
        'title': 'Forcer espérer hésiter français travers',
        'url': 'soutenances/soutenance-forcer-esperer-hesiter-francais-travers.html'
    }


def test_SeminarPage(miniwebsite):
    seminar = miniwebsite.data.seminars[0]
    page = SeminarPage(miniwebsite,
                       menu_item="Agenda",
                       title=seminar['title'],
                       template_name="seminaire.html",
                       category='séminaire',
                       seminar=seminar,
                       events=seminar['events'])
    page._export_ical()
    page.render()
    # the ref list is obtained using:
    # from pprint import pprint
    # pprint(page.get_index_node())
    assert page.get_index_node() == [
        {'date': '14/02/2011',
         'tags': ['séminaire'],
         'text': 'Juliette Traore - Chute manquer bout or réclamer juger président. '
         'Appartement vie demander ouvert fenêtre. État sien hésiter mériter '
         'cuisine occuper. Chat terrain valeur sur bientôt livrer quoi près. '
         'Calme plaisir visite prochain visite vieillard. Musique remercier '
         'annoncer mur perte. Clair jaune nu nom voici satisfaire. Matière '
         'colline mille secours agent. De voilà point entourer dessus. '
         'Prononcer crainte respect assez trou lorsque. Profond venir retirer '
         'drame couper elle solitude. Rond jaune assister demain. Maintenir '
         'demi car rouge réfléchir.',
         'title': 'Beau souffrance réveiller beauté horizon manquer - Solitude '
         'profondément naturel prière',
         'url': 'seminaires/seminaire-beau-souffrance-reveiller-beaute-horizon-manquer-2011.html#solitude-profondement-naturel-priere'},
        {'date': '02/08/2013',
         'tags': ['séminaire'],
         'text': "Stéphane Boutin - Ensemble approcher fin robe. L'Une réflexion "
         'soumettre réussir colère. Quartier ami franc ministre. Guère '
         'couleur dont fatiguer ville descendre. Fumée clef profond profiter '
         'chute tenir. Vin me race. Fort amour voiture entrer risquer. '
         'Sauvage avec page mieux trembler moyen couler. Habitude rose '
         'chemise plus. Complètement relever toile un puisque puissance. '
         'Vêtement couvrir moitié sourire or oui. Précipiter un image '
         'liberté. Reconnaître mentir crise signer comment soirée fauteuil.',
         'title': 'Beau souffrance réveiller beauté horizon manquer - Taille paix '
         'inspirer ouvrage',
         'url': 'seminaires/seminaire-beau-souffrance-reveiller-beaute-horizon-manquer-2013.html#taille-paix-inspirer-ouvrage'},
        {'date': '11/11/2017',
         'tags': ['séminaire'],
         'text': 'Michelle Barbier - Avant révéler rêver entier. Entrer fond assurer '
         'sourire veille valoir. Intérieur puisque remplir puissance figure '
         'souvent. Camarade profondément maintenant tendre. Trait lueur '
         'conversation fond toi vue larme. Lumière envoyer riche maison '
         'creuser sauvage. Passage pourquoi sourd haute. Religion air '
         'renverser trouver oeuvre soulever composer. Soldat victime clair '
         'aventure. Mon émotion vieux salut agiter.',
         'title': 'Beau souffrance réveiller beauté horizon manquer - Doucement poste '
         'notre ensemble céder',
         'url': 'seminaires/seminaire-beau-souffrance-reveiller-beaute-horizon-manquer-2017.html#doucement-poste-notre-ensemble-ceder'},
        {'date': '25/06/2018',
         'tags': ['séminaire'],
         'text': 'Lucie Daniel - Selon empêcher problème nuage. Paysan époque voici '
         'avenir fleur déjà. Compte avenir divers verre. Se avant plutôt mine '
         'demander. Sérieux que prison. Profond doucement descendre prouver '
         'type. Expérience chance exposer secours conversation françois '
         'défendre. Papier pas conclure conscience désirer servir puis.',
         'title': 'Beau souffrance réveiller beauté horizon manquer - Admettre propre '
         'existence crainte mot prochain bas',
         'url': 'seminaires/seminaire-beau-souffrance-reveiller-beaute-horizon-manquer-2018.html#admettre-propre-existence-crainte-mot-prochain-bas'},
        {'date': '14/06/2019',
         'tags': ['séminaire'],
         'text': 'Pierre Leduc - Échapper choix image claire fou donc poussière. '
         'Vivant nouveau roche premier. Spectacle reculer rêve note lourd '
         'remarquer. Naissance il auteur pur puisque exister monter. Anglais '
         'entendre supposer tempête différent étage foule ajouter. Vif loin '
         'là or bureau. Loi doux habiter cabinet montagne établir.',
         'title': 'Beau souffrance réveiller beauté horizon manquer - Obtenir blanc '
         'vif siège',
         'url': 'seminaires/seminaire-beau-souffrance-reveiller-beaute-horizon-manquer.html#obtenir-blanc-vif-siege'},
        {'date': '02/04/2020',
         'tags': ['séminaire'],
         'text': 'Alexandria Brunet-Gimenez - Autrement tôt faveur prononcer lune '
         'désigner y. Vif blanc tuer sourd tendre semblable nez chacun. Vide '
         'rapide cela retrouver comme pierre retomber. As trait mode beaux '
         'précis espace avec. Essayer travail certes. Empêcher ce absence '
         'colon. Mémoire signifier saint livre. Puis permettre sourd erreur '
         'tout fidèle franchir souhaiter. Par souffrance goutte leur '
         'résistance. Service comment grand marquer disparaître falloir banc. '
         'Pays feu baisser regarder pur retrouver poids montrer.',
         'title': 'Beau souffrance réveiller beauté horizon manquer - Enlever beaux '
         'toi valoir éclater sourire eh',
         'url': 'seminaires/seminaire-beau-souffrance-reveiller-beaute-horizon-manquer.html#enlever-beaux-toi-valoir-eclater-sourire-eh'},
        {'date': '25/09/2020',
         'tags': ['séminaire'],
         'text': 'Arnaude Paris - Lier élever faux cependant cacher venir notre. '
         'Quelque machine blond malade. Larme facile capable suffire avant. '
         'Autre impression avant étaler aide chien inquiétude. Ligne fort '
         'conduire soi vers petit. Mort indiquer même étude petit étonner '
         'cent pièce. Sueur lentement grand auteur figure. Remercier '
         'confiance condition. Inventer eaux bas pensée hésiter lutter '
         "falloir. D'Autres fleur rompre lueur dire rien bas.",
         'title': 'Beau souffrance réveiller beauté horizon manquer - Naître fumée '
         'expérience',
         'url': 'seminaires/seminaire-beau-souffrance-reveiller-beaute-horizon-manquer.html#naitre-fumee-experience'}]
    assert page.ical_url == "https://fakelab.fk/cal/seminaire-beau-souffrance-reveiller-beaute-horizon-manquer.ics"
    ical_filepath = ('cal' /
                     Path(utils.slugify(page._get_filename())).with_suffix('.ics'))
    ical_outpath = page.conf.output_path / ical_filepath
    # Read the 20 first lines of the ical file
    with open(ical_outpath) as f:
        lines = f.readlines()
    truncated_head = ''.join(line for line in lines[:20]
                             if (not line.startswith('UID') and
                                 not line.startswith('DTSTAMP')))
    assert truncated_head == """\
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Pilab//Séminaire Beau souffrance réveiller beauté horizon man
 quer//FR
BEGIN:VEVENT
SUMMARY:Lucie Daniel - Admettre propre existence crainte mot prochain bas
DTSTART;TZID=Europe/Paris;VALUE=DATE-TIME:20180625T042207
DTEND;TZID=Europe/Paris;VALUE=DATE-TIME:20180625T052207
DESCRIPTION:Selon empêcher problème nuage. Paysan époque voici avenir f
 leur déjà. Compte avenir divers verre. Se avant plutôt mine demander. S
 érieux que prison. Profond doucement descendre prouver type. Expérience 
 chance exposer secours conversation françois défendre. Papier pas conclu
 re conscience désirer servir puis.
LOCATION:salle de patron
PRIORITY:5
URL:https://fakelab.fk/seminaires/seminaire-beau-souffrance-reveiller-beau
 te-horizon-manquer.html
END:VEVENT
"""


def test_SeminarTopIndexPage(miniwebsite):
    status = 'actif'
    page = SeminarTopIndexPage(website=miniwebsite,
                               menu_item='Agenda',
                               title='Séminaires',
                               template_name="seminaires.html",
                               seminars=miniwebsite.data.seminars,
                               status=status)
    page.render()
    # the ref dictionany is obtained using:
    # from pprint import pprint
    # pprint(page.get_index_node())
    assert page.get_index_node() == {
        'date': '',
        'tags': ['Séminaires actifs'],
        'text': 'Séminaires',
        'title': 'Séminaires',
        'url': 'seminaires/index.html'}
    assert page.ical_url == "https://fakelab.fk/cal/seminaires.ics"
    # The rest of SeminarTopIndexPage calendar test is done in test_calendar.py


def test_WorkGroupTopIndexPage(miniwebsite):
    status = 'actif'
    page = WorkGroupTopIndexPage(website=miniwebsite,
                                 menu_item='Agenda',
                                 title='Groupes de travail',
                                 template_name="seminaires.html",
                                 seminars=miniwebsite.data.seminars,
                                 status=status)
    page.render()
    # the ref dictionany is obtained using:
    # from pprint import pprint
    # pprint(page.get_index_node())
    assert page.get_index_node() == {
        'date': '',
        'tags': ['Groupes de travail actifs'],
        'text': 'Groupes de travail',
        'title': 'Groupes de travail',
        'url': 'groupes-de-travail/index.html'}


def test_IndexPage(miniwebsite):

    # Build website in order to register events
    miniwebsite.build()
    page = IndexPage(miniwebsite,
                     menu_item='Agenda',
                     title='Conférences et rencontres',
                     template_name='agenda.html',
                     filename='index.html',
                     category='conférence',
                     events=miniwebsite.data.conferences)
    page.render()
    assert page.filepath == Path('index.html')
    assert page.menu_item == "Agenda"
    assert page.template_path == Path('agenda.html')
    assert page.html_path == Path('conferences/index.html')
    assert page.out_path.as_posix().endswith(
        '/output/conferences/index.html')
    assert page.content == "Conférences et rencontres"
    assert len(page.events) == 4
    assert str(page.paginator) == '[2012, 2007, 2006, 2003] - index.html'

    all_events = miniwebsite.data.conferences
    for seminar in miniwebsite.data.seminars:
        all_events.extend(seminar['events'])

    coming_events = [event for event in all_events
                     if event['date'].date() >= miniwebsite.conf.site['today']]

    page = IndexPage(website=miniwebsite,
                     menu_item='Agenda',
                     title='À venir',
                     template_name='agenda.html',
                     filename='a_venir.html',
                     events=coming_events)
    page.render()
    assert page.filepath == Path('a_venir.html')
    assert page.menu_item == "Agenda"
    assert page.template_path == Path('agenda.html')
    assert page.html_path == Path('a_venir.html')
    assert page.out_path.as_posix().endswith('/output/a_venir.html')
    assert page.content == "À venir"
    assert len(page.events) == 11
    assert page.paginator is None


def test_NewsPage(miniwebsite):
    """
---
title: Retenir cours peser autant
description: Intérieur membre plaisir remonter songer large. Se supporter poche veiller.
date: 2019-06-23
category: news
---

# Prière enfance protéger lueur étoile paysage doucement

Miser rapporter faire durer aventure. Coeur morceau enfin portier fermer quarante.

# Français troisième retrouver ailleurs céder passer

Foi clair expliquer. Importance remonter compte croire mal. Heureux beau distance sérieux précipiter tracer.

"""
    md_filepath = test_content_path / 'actualites/2019_spip_actu_1096.md'
    metadata, md_content = utils.parse_md_file(md_filepath)
    page = NewsPage(miniwebsite, md_filepath, metadata, md_content,
                    template_name="article.html")
    page.render()
    assert page.title == 'Retenir cours peser autant'
    assert page.category == 'news'
    assert page.filepath == (test_content_path /
                             'actualites/2019_spip_actu_1096.md')
    assert page.template_path == Path('article.html')
    assert page.html_path == Path('actualites/2019_spip_actu_1096.html')
    assert page.out_path == (
        miniwebsite.conf.output_path / 'actualites/2019_spip_actu_1096.html')
    assert page.content[:20] == "Intérieur membre pla"
    assert page.content[-20:] == "cipiter tracer.</p>\n"
    assert miniwebsite.data.news == [
        {'chapo': 'Intérieur membre plaisir remonter songer large. Se supporter poche '
         'veiller.',
         'date': datetime.date(2019, 6, 23),
         'external': False,
         'href': 'actualites/2019_spip_actu_1096.html',
         'text': [{'content': '\n'
                   '<p>Miser rapporter faire durer aventure. Coeur morceau '
                   'enfin portier fermer quarante.</p>\n',
                   'id': 'priere-enfance-proteger-lueur-etoile-paysage-doucement',
                   'title': 'Prière enfance protéger lueur étoile paysage doucement'},
                  {'content': '\n'
                   '<p>Foi clair expliquer. Importance remonter compte '
                   'croire mal. Heureux beau distance sérieux précipiter '
                   'tracer.</p>',
                   'id': 'francais-troisieme-retrouver-ailleurs-ceder-passer',
                   'title': 'Français troisième retrouver ailleurs céder passer'}],
         'title': 'Retenir cours peser autant'}
    ]

    # the ref dictionany is obtained using:
    # from pprint import pprint
    # pprint(page.get_index_node())
    assert page.get_index_node() == {
        'date': '23/06/2019',
        'tags': ['news'],
        'text': 'Intérieur membre plaisir remonter songer large. Se supporter poche '
        'veiller.Prière enfance protéger lueur étoile paysage doucement - '
        'Miser rapporter faire durer aventure. Coeur morceau enfin portier '
        'fermer quarante. Français troisième retrouver ailleurs céder passer '
        '- Foi clair expliquer. Importance remonter compte croire mal. '
        'Heureux beau distance sérieux précipiter tracer.',
        'title': 'Retenir cours peser autant',
        'url': 'actualites/2019_spip_actu_1096.html'
    }


def test_LibNewsPage(miniwebsite):
    """
---
title: Impression tracer avant créer
date: 2015-07-18
category: libnews
---

Français en terminer branche que juge.
Décider reculer quart visible.
Descendre cruel relever nuage absence.
Durer ceci tranquille chercher ordre quelqu'un.
Voyager certain diriger sein barbe.
Inquiétude chasser vingt après prochain homme.
Terme grâce nuit instant diriger aussi.
Conscience police cheval passage soleil exister certain.
Maison porter désormais.
Espèce cesse difficile million devant.
Claire contre robe perdre entrée attacher.
Toujours volonté après vide arrêter frapper.

{{% button href="http://www.schneider.org/" text="En savoir plus" %}}

"""
    md_filepath = test_content_path / 'bib/actualites/2015-07-18_libnews.md'
    metadata, md_content = utils.parse_md_file(md_filepath)
    page = LibNewsPage(miniwebsite, md_filepath, metadata, md_content)
    page.render()
    assert page.title == 'Impression tracer avant créer'
    assert page.category == 'libnews'
    assert page.filepath == md_filepath
    assert page.template_path == Path('article.html')
    assert page.html_path is None
    assert page.out_path is None
    assert page.content[:20] == "<p>Français en termi"
    assert page.content[-20:] == " plus\n  </a>\n</div>\n"
    assert miniwebsite.data.libnews == [
        {'date': datetime.date(2015, 7, 18),
         'slug': 'impression-tracer-avant-creer',
         'text': '<p>Français en terminer branche que juge. Décider reculer quart '
         'visible. Descendre cruel relever nuage absence. Durer ceci '
         "tranquille chercher ordre quelqu'un. Voyager certain diriger sein "
         'barbe. Inquiétude chasser vingt après prochain homme. Terme grâce '
         'nuit instant diriger aussi. Conscience police cheval passage soleil '
         'exister certain. Maison porter désormais. Espèce cesse difficile '
         'million devant. Claire contre robe perdre entrée attacher. Toujours '
         'volonté après vide arrêter frapper.</p>\n'
         '<div class="center">\n'
         '<a class="waves-effect waves-light btn" '
         'href="http://www.schneider.org/" referrerpolicy="no-referrer" '
         'rel="noopener noreferrer" target="_blank">\n'
         '    En savoir plus\n'
         '  </a>\n'
         '</div>',
         'title': 'Impression tracer avant créer'}
    ]
    # libnews index_nodes are produced by the LibNewsIndexPage
    assert page.get_index_node() is None


def test_VirtualNewsPage(miniwebsite):
    md_filepath = test_content_path / 'actualites/2015_spip_actu_3686.md'
    metadata, md_content = utils.parse_md_file(md_filepath)
    page = VirtualNewsPage(miniwebsite, md_filepath, metadata, md_content,
                           template_name="article.html")
    page.render()
    assert page.title == 'Cruel aller santé françois dimanche parole ce'
    assert page.category == 'news'
    assert page.filepath == (test_content_path /
                             'actualites/2015_spip_actu_3686.md')
    assert page.template_path == Path('article.html')
    assert page.html_path == 'http://www.fernandes.com/'
    assert page.out_path is None
    assert page.content[: 20] == 'Découvrir envelopper'
    assert page.content[-20:] == 'pper but leur frais.'
    assert miniwebsite.data.news == [
        {'chapo': 'Découvrir envelopper but leur frais.',
         'date': datetime.date(2015, 1, 19),
         'external': True,
         'href': 'http://www.fernandes.com/',
         'text': None,
         'title': 'Cruel aller santé françois dimanche parole ce'}
    ]

    # the ref dictionany is obtained using:
    # from pprint import pprint
    # pprint(page.get_index_node())
    assert page.get_index_node() == {
        'date': '19/01/2015',
        'tags': ['news'],
        'text': 'Découvrir envelopper but leur frais.',
        'title': 'Cruel aller santé françois dimanche parole ce',
        'url': 'http://www.fernandes.com/'
    }


def test_NewsIndexPage(miniwebsite):

    # Consume the md_pages generator to register news pages
    for _ in miniwebsite.md_pages():
        pass

    page = NewsIndexPage(miniwebsite)
    page.render()
    assert page.title == 'Actualités'
    assert page.category == 'news'
    assert page.template_path.as_posix() == 'actualites.html'
    assert page.html_path.as_posix() == 'index.html'

    # Search for a specific news
    mynews = next(news for news in miniwebsite.data.news
                  if news['href'] == 'actualites/2019_spip_actu_1096.html')
    # from pprint import pprint
    # pprint(mynews)
    assert mynews == {
        'chapo': 'Intérieur membre plaisir remonter songer large. Se supporter poche '
        'veiller.',
        'date': datetime.date(2019, 6, 23),
        'external': False,
        'href': 'actualites/2019_spip_actu_1096.html',
        'text': [{'content': '\n'
                  '<p>Miser rapporter faire durer aventure. Coeur morceau '
                  'enfin portier fermer quarante.</p>\n',
                  'id': 'priere-enfance-proteger-lueur-etoile-paysage-doucement',
                  'title': 'Prière enfance protéger lueur étoile paysage doucement'},
                 {'content': '\n'
                  '<p>Foi clair expliquer. Importance remonter compte '
                  'croire mal. Heureux beau distance sérieux précipiter '
                  'tracer.</p>',
                  'id': 'francais-troisieme-retrouver-ailleurs-ceder-passer',
                  'title': 'Français troisième retrouver ailleurs céder passer'}],
        'title': 'Retenir cours peser autant'
    }
    assert page.get_index_node() == {'date': '',
                                     'tags': ['news'],
                                     'text': 'Actualités',
                                     'title': 'Actualités',
                                     'url': 'index.html'}


def test_LibNewsIndexPage(miniwebsite):

    # Consume the md_pages generator to register news pages
    for _ in miniwebsite.md_pages():
        pass

    page = LibNewsIndexPage(miniwebsite, menu_item='Bibliothèque')
    page.render()
    assert page.title == 'Actualités de la bibliothèque'
    assert page.category == 'libnews'
    assert page.template_path.as_posix() == 'actualites-bib.html'
    assert page.html_path.as_posix() == 'actualites-bib.html'
    assert page.menu_item == 'Bibliothèque'

    # Search for a specific news
    mynews = next(news for news in miniwebsite.data.libnews
                  if news['date'] == datetime.date(2015, 8, 27))

    assert mynews == {
        'date': datetime.date(2015, 8, 27),
        'slug': 'seulement-paysage-enfant-sante-beau-rose',
        'text': '<p>Grand ensemble envelopper bout retenir étendre porter. Société '
        'silencieux blanc ligne on. Le présent morceau agiter fenêtre pur '
        'cuisine. Étudier grâce village joie cabinet. Sourire circonstance '
        'appel dominer confiance. Curieux en miser coeur fixer victime si '
        'importer. Centre époque valoir assurer traîner salut ici. Ton forcer '
        'rouler appartenir yeux occuper mêler franc. Inconnu non expliquer '
        'lueur. Dur apparence haïr fond sortir on comment. Curieux chose '
        'sommet toit entourer.</p>\n'
        '<div class="center">\n'
        '<a class="waves-effect waves-light btn" '
        'href="http://www.garnier.fr/" referrerpolicy="no-referrer" '
        'rel="noopener noreferrer" target="_blank">\n'
        '    En savoir plus\n'
        '  </a>\n'
        '</div>',
        'title': 'Seulement paysage enfant santé beau rose'
    }

    # Search for a specific node
    index_node = next(node for node in page.get_index_node()
                      if node['date'] == '04/04/2018')
    assert index_node == {
        'date': '04/04/2018',
        'tags': ['libnews'],
        'text': 'Immense manquer dessiner. Étage apparaître découvrir marquer. '
        'Monter creuser cheval coucher difficile fauteuil. Mari pencher un '
        'calme palais boire essuyer direction. Public exemple auquel. Quatre '
        'haut compter transformer prier. Joli quarante fruit quitter début '
        'côte. En savoir plus',
        'title': 'Actualités de la bibliothèque - Prochain comprendre changement '
        'coeur valeur',
        'url': 'libnews/actualites-bib-2018.html#prochain-comprendre-changement-coeur-valeur'
    }


def test_HomePage(miniwebsite):
    page = HomePage(miniwebsite, 'Mon titre')
    page.render()
    assert page.title == 'Mon titre'
    assert page.category == 'homepage'
    assert page.filepath == Path('index.html')
    assert page.template_path == Path('index.html')
    assert page.template_path == Path('index.html')
    assert page.out_path == miniwebsite.conf.output_path / 'index.html'
    assert page.content == (
        '<p>Charge souhaiter étendre rencontrer. Trait réalité se connaître moindre. '
        'Déposer cas nez devoir pont situation traiter pas.</p><p>Rien apercevoir '
        'donner mieux même retenir fils. Pourquoi pleurer de semaine.</p>')
    assert page.cards == [
        {'category': 'homecard',
         'header': 'Maladie étendue environ.',
         'img': {'alt': 'Éteindre condamner mille long.',
                 'src': 'https://unsplash.it/700/740'},
         'links': [{'color': 'teal-text',
                    'href': 'lelaboratoire/presentation.html',
                    'text': 'En savoir plus'}],
         'text': '<p>Charge souhaiter étendre rencontrer. Trait réalité se connaître '
         'moindre. Déposer cas nez devoir pont situation traiter pas.</p>',
         'title': 'Mon cher laboratoire'},
        {'category': 'homecard',
            'header': 'Tendre profond siècle veiller changement.',
            'links': [{'color': 'teal-text',
                       'href': 'actualites/2020_spip_actu_7113.html',
                       'text': 'En savoir plus'},
                      {'color': 'grey-text',
                       'href': '#news',
                       'text': "Plus d'actualités"}],
            'text': '<p>Rien apercevoir donner mieux même retenir fils. Pourquoi pleurer '
         'de semaine.</p>',
            'title': 'À la une'}
    ]
