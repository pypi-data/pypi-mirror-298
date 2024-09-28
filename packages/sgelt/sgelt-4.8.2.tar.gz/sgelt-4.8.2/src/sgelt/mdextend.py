"""Customized markdown extension"""

from markdown.treeprocessors import Treeprocessor
from markdown.extensions import Extension


class TableProcessor(Treeprocessor):
    def run(self, root):
        for element in root.iter('table'):
            element.set("class", "responsive-table")


class TableExtension(Extension):
    """Add class="responsive-table" to all table elements"""
    def extendMarkdown(self, md):
        md.treeprocessors.register(TableProcessor(md), 'tableextension', 15)
