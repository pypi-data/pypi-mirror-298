"""Parse markdown content"""

import bs4
import shortcodes

from .utils import md_slugify, md


def get_sections(md_content: str) -> list:
    """
    Parse markdown string to build a list of section dicts:
    {
        'title': h2 title,
        'id': slugify(title),
        'content': section_content
    }
    """

    # Important for performance:
    # see https://python-markdown.github.io/extensions/api/#registerextension
    md.reset()
    html = md.convert(md_content)
    # Build section dict
    soup = bs4.BeautifulSoup(html, "html.parser")
    section_dict = {}

    # If section does not start with a h2 tag
    no_h2_section = ''
    for tag in soup:
        if tag.name == 'h2':
            break
        else:
            no_h2_section += str(tag)

    if no_h2_section:
        section_dict[''] = no_h2_section

    # Parse the rest
    for h2 in soup.find_all('h2'):
        title = h2.text
        section_dict[title] = ''
        for tag in h2.next_siblings:
            if tag.name == 'h2':
                break
            section_dict[title] += str(tag)

    sections = []
    for title, content in section_dict.items():
        section = {'title': title, 'id': md_slugify(title), 'content': content}
        sections.append(section)

    return sections, md.toc_tokens


@shortcodes.register("team_members")
def team_members_handler(_, kwargs: dict, context) -> str:
    """
    A short code to inject team members markdown.
    Usage:
    {{% team_members permanent=True %}}
    """
    env = context['page'].conf.env

    team_name = context['page'].metadata['team']
    # json lib does not convert json boolean so:
    permanent = bool(kwargs['permanent'] == 'True')
    all_members = context['data'].teams[team_name]['members']

    members = [member for member in all_members
               if member['permanent'] == permanent]

    template_string = """\
{%- for member in members %}
{%- if member.url %}
- [{{ member.firstname }} {{ member.name }}]({{ member.url }}){{ ', {}'\
.format(member.status) if member.status }}
{%- else %}
- {{ member.firstname }} {{ member.name }}{{ ', {}'.format(member.status)\
if member.status }}
{%- endif -%}
{%- endfor -%}
"""
    template = env.from_string(template_string)
    return template.render(members=members)


@shortcodes.register("team_seminars")
def team_seminars_handler(_, kwargs: dict, context) -> str:
    """
    A shortcode to inject links to the seminars organized by the team.
    Usage:
    {{% team_seminars %}}
    """
    env = context['page'].conf.env

    team_seminars = context['page'].team_seminars
    sem_template = (r"le {{ seminar.type |lower }} [{{ seminar.title }}]"
                    r"(../{{ seminar.html_path }})")
    if len(team_seminars) == 1:
        template_string = f"L'équipe anime {sem_template}."
        template = env.from_string(template_string)
        return template.render(seminar=team_seminars[0])
    else:
        template_string = """L'équipe anime :
{{% for seminar in seminars %}}
- {}
{{%- endfor -%}}
""".format(sem_template)
        template = env.from_string(template_string)
        return template.render(seminars=team_seminars)


@shortcodes.register("button")
def button_handler(_, kwargs: dict, context) -> str:
    """
    A shortcode to inject an html button.
    Usage:
    {{% button href="attachments/file.pdf" text="Document PDF" \
icon="cloud_download" %}}
    """
    href = kwargs['href']
    text = kwargs['text']
    icon = kwargs.get('icon')
    btn_class = kwargs.get('btn_class', 'btn')

    env = context['page'].conf.env

    template_string = """\
<div class="center">
  <a class="waves-effect waves-light {{ btn_class }}" href="{{ href }}" \
{{ href | external_url }}>
    {{ '<i class="material-icons right" aria-hidden="true">{}</i>'\
.format(icon) if icon }}{{ text }}
  </a>
</div>"""
    template = env.from_string(template_string)
    return template.render(href=href, text=text, icon=icon,
                           btn_class=btn_class)
