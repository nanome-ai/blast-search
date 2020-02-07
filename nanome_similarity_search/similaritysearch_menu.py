import nanome
from nanome.util import Logs
from nanome.util import Color

import os

class SimilaritySearchMenu():
    def __init__(self, similaritysearch_plugin):
        self._menu = similaritysearch_plugin.menu
        self._plugin = similaritysearch_plugin
        self._selected_query = None

    def _request_refresh(self):
        self._plugin.request_refresh()

    def change_complex_list(self,complex_list):
        Logs.debug("change complex list called")

        self._query_list = []

        def query_pressed(button):
            self._selected_query = button.complex
            Logs.debug("complex ",self._selected_query, " selected")

        for complex in complex_list:
            clone = self._complex_item_prefab.clone()
            ln_btn = clone.get_children()[0]
            btn = ln_btn.get_content()
            btn.text.value.set_all(complex.name)
            btn.complex = complex
            btn.register_pressed_callback(query_pressed)
            self._query_list.append(clone)
        
        Logs.debug("query list is:", self._query_list)
        self._show_list.items = self._query_list
        self._plugin.update_content(self._show_list)

    def build_menu(self):
        
        menu = nanome.ui.Menu.io.from_json(os.path.join(os.path.dirname(__file__), 'SimilaritySearchMenu.json'))
        self._plugin.menu = menu

        self._show_list = menu.root.find_node("Input List", True).get_content()

        # Create a prefab that will be used to populate the lists
        self._complex_item_prefab = nanome.ui.LayoutNode()
        self._complex_item_prefab.layout_orientation = nanome.ui.LayoutNode.LayoutTypes.horizontal
        child = self._complex_item_prefab.create_child_node()
        child.name = "complex_button"
        prefabButton = child.add_new_button()
        prefabButton.text.active = True

        
