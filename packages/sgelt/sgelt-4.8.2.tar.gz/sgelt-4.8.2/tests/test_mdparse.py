from sgelt import mdparse, pages, utils

section_0 = """\
L’Institut est situé sur le campus de l'Esplanade, qui est proche du centre-ville.

Son adresse exacte est :

> Institut de Recherche Mathématique Avancée,
> 7 rue René Descartes,
> 67084 Strasbourg Cedex

"""

sections_1_2 = """\
## Plans et cartes

Vous pouvez consulter [StrasMap](https://strasmap.eu/Home).

## Comment venir

### À partir de la gare

- À pied en quarante minutes munis d’un plan de Strasbourg (disponible à l'office du tourisme dans la gare)
- Taxi
- TRAM : ligne C direction "Neuhof, Rodolphe Reuss", arrêt "Universités".
"""

section_list = [{
    'title': '',
    'id': '',
    'content': '''\
<p>L’Institut est situé sur le campus de l'Esplanade, qui est proche du centre-ville.</p>
<p>Son adresse exacte est :</p>
<blockquote>\n<p>Institut de Recherche Mathématique Avancée,
7 rue René Descartes,\n67084 Strasbourg Cedex</p>
</blockquote>
'''},
    {
    'title': 'Plans et cartes',
    'id': 'plans-et-cartes',
    'content': '''
<p>Vous pouvez consulter <a href="https://strasmap.eu/Home" referrerpolicy="no-referrer" rel="noopener noreferrer" target="_blank">StrasMap</a>.</p>
'''
},
    {
    'title': 'Comment venir',
    'id': 'comment-venir',
    'content': '''
<h3 id="a-partir-de-la-gare">À partir de la gare</h3>
<ul>
<li>À pied en quarante minutes munis d’un plan de Strasbourg (disponible à l'office du tourisme dans la gare)</li>
<li>Taxi</li>
<li>TRAM : ligne C direction "Neuhof, Rodolphe Reuss", arrêt "Universités".</li>
</ul>'''
}]


def test_get_sections():
    assert mdparse.get_sections(section_0 + sections_1_2)[0] == section_list
    assert mdparse.get_sections(sections_1_2)[0] == section_list[1:]


def test_tables():
    """Test that markdown conversion add class attributes to table elements"""
    s = """
a | table
--- | ---
spam | egg
"""

    expected = """\
<table class="responsive-table">
<thead>
<tr>
<th>a</th>
<th>table</th>
</tr>
</thead>
<tbody>
<tr>
<td>spam</td>
<td>egg</td>
</tr>
</tbody>
</table>\
"""
    assert utils.md.convert(s) == expected


class FakeMdPage:
    """A Mockup class for MdPage"""
    parser = pages.MdPage.parser
    _parse_shortcodes = pages.MdPage._parse_shortcodes

    def __init__(self, website, team=None):
        self.conf = website.conf
        self.data = website.data
        self.category = 'team' if team else None
        self.metadata = {'team': team}
        self.team_seminars = pages.MdPage._get_team_seminars(self)


def test_shortcode_team_members(miniwebsite):
    md_content = """\
# Membres

## Membres permanents

{{% team_members permanent=True %}}

## Membres non permanents

{{% team_members permanent=False %}}

"""
    expected = """\
# Membres

## Membres permanents


- Marguerite Le Roux, Chargée de recherche
- [Océane Klein](https://fake.fr/~klein/), Directrice de recherche émérite
- [Amélie Samson](https://fake.fr/~samson/), Ingénieure
- Cécile Millet, Maîtresse de conférences émérite
- [Cécile Verdier](https://fake.fr/~verdier/), Maîtresse de conférences émérite
- [Audrey Duval](https://fake.fr/~duval/), Professeure

## Membres non permanents


- Jacques Ribeiro, ATER
- Adrien Germain, ATER
- [Lucy Foucher](https://fake.fr/~foucher/), Invitée

"""

    md_page = FakeMdPage(miniwebsite, 'TU')
    assert md_page._parse_shortcodes(md_content) == expected


def test_shortcode_team_seminars(miniwebsite):
    miniwebsite.build()
    md_content = """\

{{% team_seminars %}}

"""
    md_page = FakeMdPage(miniwebsite, 'TU')
    expected = """
L'équipe anime :

- le groupe de travail [Inspirer sauter fatigue croix appuyer](../groupes-de-travail/groupe-de-travail-inspirer-sauter-fatigue-croix-appuyer.html)
- le séminaire [Donc repas éternel sein travers pénétrer](../seminaires/seminaire-donc-repas-eternel-sein-travers-penetrer.html)

"""
    assert md_page._parse_shortcodes(md_content) == expected

    md_page = FakeMdPage(miniwebsite, 'RA')
    expected = """
L'équipe anime le séminaire [Beau souffrance réveiller beauté horizon manquer](../seminaires/seminaire-beau-souffrance-reveiller-beaute-horizon-manquer.html).

"""
    md_page = FakeMdPage(miniwebsite, 'RA')
    assert md_page._parse_shortcodes(md_content) == expected

    md_page = FakeMdPage(miniwebsite, 'WG')
    expected = """
L'équipe anime le séminaire [Donc repas éternel sein travers pénétrer](../seminaires/seminaire-donc-repas-eternel-sein-travers-penetrer.html).

"""
    assert md_page._parse_shortcodes(md_content) == expected


def test_shortcode_button(miniwebsite):
    md_page = FakeMdPage(miniwebsite)

    # Test with icon
    md_content = """\
{{% button href="attachments/file.pdf" icon="cloud_download" text="Download PDF" %}}
"""
    expected = """\
<div class="center">
  <a class="waves-effect waves-light btn" href="attachments/file.pdf" >
    <i class="material-icons right" aria-hidden="true">cloud_download</i>Download PDF
  </a>
</div>
"""
    assert md_page._parse_shortcodes(md_content) == expected

    # Test without icon
    md_content = """\
{{% button href="attachments/file.pdf" text="Download PDF" %}}
"""
    expected = """\
<div class="center">
  <a class="waves-effect waves-light btn" href="attachments/file.pdf" >
    Download PDF
  </a>
</div>
"""
    assert md_page._parse_shortcodes(md_content) == expected

    # Test with btn-class
    md_content = """\
{{% button href="attachments/file.pdf" text="Download PDF" btn_class="btn-small" %}}
"""
    expected = """\
<div class="center">
  <a class="waves-effect waves-light btn-small" href="attachments/file.pdf" >
    Download PDF
  </a>
</div>
"""
    assert md_page._parse_shortcodes(md_content) == expected

    # Test with external url
    md_content = """\
{{% button href="https://fake.fr" text="Go to URL" %}}
"""
    expected = """\
<div class="center">
  <a class="waves-effect waves-light btn" href="https://fake.fr" referrerpolicy="no-referrer" rel="noopener noreferrer" target="_blank">
    Go to URL
  </a>
</div>
"""
    assert md_page._parse_shortcodes(md_content) == expected
