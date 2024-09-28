"""Test a full website build"""
import filecmp


def test_copy_payload(miniwebsite, tmp_path):
    miniwebsite.copy_payload()

    paths = {}
    for path in miniwebsite.conf.static_payload:
        dst_dir = miniwebsite.conf.output_path / path
        paths[path.as_posix()] = set(path.relative_to(tmp_path).as_posix()
                                     for path in dst_dir.glob('**/*'))

    expected = {
        'css': {'output/css/materialize.css',
                'output/css/materialize.min.css',
                'output/css/style.css'},
        'img': {'output/img/favicon.ico',
                'output/img/iss.jpg',
                'output/img/logo_jinja.png',
                'output/img/logo_materialize.png',
                'output/img/logo_pi.png',
                'output/img/logo_python.png'},
        'js': {'output/js/delaunay.js',
               'output/js/init.js',
               'output/js/lunr-search-result.js',
               'output/js/lunr.js',
               'output/js/materialize.js',
               'output/js/materialize.min.js',
               'output/js/parallax.js',
               'output/js/parallax.min.js'}
    }

    assert paths == expected


def get_common_files(dcmp, s=''):
    for name in dcmp.common_files:
        s += f"common_files {name} found in {dcmp.left} and {dcmp.right}"
    for sub_dcmp in dcmp.subdirs.values():
        get_common_files(sub_dcmp, s)


def test_copy_attachments(miniwebsite):
    miniwebsite.copy_attachments()
    src_dir = miniwebsite.conf.content_path
    dst_dir = miniwebsite.conf.output_path
    dcmp = filecmp.dircmp(src_dir, dst_dir)

    assert dcmp.common_dirs == ['lelaboratoire']
    for sub_dcmp in dcmp.subdirs.values():
        assert sub_dcmp.common_dirs == ['attachments', 'img']


def test_minisite(miniwebsite):
    """Test mini site construction"""
    output_path = miniwebsite.conf.output_path
    miniwebsite.build()

    def check_expected_files(expected_filenames: str, extension: str):
        # Create a set of all files from output dir with given extension
        filenames = set(
            path.relative_to(miniwebsite.conf.output_path).as_posix()
            for path in output_path.glob(f'**/*.{extension}'))
        assert filenames == set(expected_filenames.split())

    # Created using:
    # for file in sorted(path.relative_to(output_path)
    #                    for path in output_path.glob('**/*.html')):
    #     print(file.as_posix())
    expected_html_files = """
a_venir.html
actualites/2015_spip_actu_3686.html
actualites/2017_spip_actu_9975.html
actualites/2018_spip_actu_7076.html
actualites/2018_spip_actu_8375.html
actualites/2019_spip_actu_1096.html
actualites/2020_spip_actu_7113.html
actualites/index-2015.html
actualites/index-2017.html
actualites/index-2018.html
actualites/index.html
bib/infos_pratiques.html
conferences/ah-simple-tourner-dos-parent-8067.html
conferences/art-reculer-calmer-retirer-subir-chaud-sein-3050.html
conferences/inconnu-non-expliquer-lueur-643.html
conferences/retourner-trois-passer-calme-pleurer-si-4764.html
conferences/index-2003.html
conferences/index-2006.html
conferences/index-2007.html
conferences/index.html
groupes-de-travail/groupe-de-travail-inspirer-sauter-fatigue-croix-appuyer-2010.html
groupes-de-travail/groupe-de-travail-inspirer-sauter-fatigue-croix-appuyer.html
groupes-de-travail/groupe-de-travail-traiter-joindre-car-reve-froid-demain-fixer-2008.html
groupes-de-travail/groupe-de-travail-traiter-joindre-car-reve-froid-demain-fixer-2015.html
groupes-de-travail/groupe-de-travail-traiter-joindre-car-reve-froid-demain-fixer.html
groupes-de-travail/index.html
groupes-de-travail/passes.html
index.html
lelaboratoire/venir.html
lelaboratoire/organisation.html
lelaboratoire/presentation.html
libnews/actualites-bib-2015.html
libnews/actualites-bib-2018.html
libnews/actualites-bib.html
pages/mentions-legales.html
search.html
soutenances/soutenance-forcer-esperer-hesiter-francais-travers.html
soutenances/soutenance-vol-voix-secours-lien-nuit-avance.html
soutenances/soutenance-eclat-gouvernement-ne-rever-autrefois.html
soutenances/index-2004.html
soutenances/index-2011.html
soutenances/index.html
seminaires/index.html
seminaires/passes.html
seminaires/seminaire-beau-souffrance-reveiller-beaute-horizon-manquer-2011.html
seminaires/seminaire-beau-souffrance-reveiller-beaute-horizon-manquer-2013.html
seminaires/seminaire-beau-souffrance-reveiller-beaute-horizon-manquer-2017.html
seminaires/seminaire-beau-souffrance-reveiller-beaute-horizon-manquer-2018.html
seminaires/seminaire-beau-souffrance-reveiller-beaute-horizon-manquer.html
seminaires/seminaire-cinquante-tot-retrouver-douceur-2006.html
seminaires/seminaire-cinquante-tot-retrouver-douceur-2008.html
seminaires/seminaire-cinquante-tot-retrouver-douceur-2009.html
seminaires/seminaire-cinquante-tot-retrouver-douceur-2010.html
seminaires/seminaire-cinquante-tot-retrouver-douceur.html
seminaires/seminaire-donc-repas-eternel-sein-travers-penetrer.html
equipes/ra.html
equipes/susu.html
equipes/tu.html
equipes/wg.html
"""
    check_expected_files(expected_html_files, 'html')

    expected_png_files = """
img/logo_jinja.png
img/logo_materialize.png
img/logo_pi.png
img/logo_python.png
lelaboratoire/img/fake.png
"""
    check_expected_files(expected_png_files, 'png')

    expected_js_files = """
js/delaunay.js
js/init.js
js/lunr-search-result.js
js/lunr.js
js/materialize.js
js/materialize.min.js
js/parallax.js
js/parallax.min.js
lunr_content.js
"""
    check_expected_files(expected_js_files, 'js')

    expected_css_files = """
css/materialize.css
css/materialize.min.css
css/style.css
    """
    check_expected_files(expected_css_files, 'css')

    expected_pdf_files = """
lelaboratoire/attachments/fake.pdf
"""
    check_expected_files(expected_pdf_files, 'pdf')
