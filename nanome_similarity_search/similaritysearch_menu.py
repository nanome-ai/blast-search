import nanome
from nanome.util import Logs
from nanome.util import Color

import os

class SimilaritySearchMenu():
    def __init__(self, similaritysearch_plugin):
        self._menu = similaritysearch_plugin.menu
        self._plugin = similaritysearch_plugin

    def build_menu(self):
        menu = nanome.ui.Menu.io.from_json(os.path.join(os.path.dirname(__file__), 'SimilaritySearchMenu.json'))
        self._plugin.menu = menu
