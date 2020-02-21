import nanome
from nanome.util import Logs
from nanome.util import Color

import os

class SimilaritySearchMenu():
    def __init__(self, similaritysearch_plugin):
        self.menu = similaritysearch_plugin.menu
        self.plugin = similaritysearch_plugin
        self.selected_query = None

    def _request_refresh(self):
        self.plugin.request_refresh()

    def change_complex_list(self,complex_list):
        Logs.debug("change complex list called")

        self.query_list = []

        def query_pressed(button):
            self.selected_query = button.complex
            button.selected = not button.selected
            if button.selected:
                self.selected_query = button.complex
            else:
                self.selected_query = None
            self.plugin.update_content(button)

        for complex in complex_list:
            clone = self.complex_item_prefab.clone()
            ln_btn = clone.get_children()[0]
            btn = ln_btn.get_content()
            btn.text.value.set_all(complex.name)
            btn.complex = complex
            btn.register_pressed_callback(query_pressed)
            self.query_list.append(clone)
        
        Logs.debug("query list is:", self.query_list)
        self.show_list.items = self.query_list
        self.plugin.update_content(self.show_list)

    def build_menu(self):
        def search_button_pressed_callback(button):
            self.plugin.search_blast()
        
        menu = nanome.ui.Menu.io.from_json(os.path.join(os.path.dirname(__file__), 'SimilaritySearchMenu.json'))
        self.plugin.menu = menu

        self.show_list = menu.root.find_node("Input List", True).get_content()

        # Create a prefab that will be used to populate the lists
        self.complex_item_prefab = nanome.ui.LayoutNode()
        self.complex_item_prefab.layout_orientation = nanome.ui.LayoutNode.LayoutTypes.horizontal
        child = self.complex_item_prefab.create_child_node()
        child.name = "complex_button"
        prefabButton = child.add_new_button()
        prefabButton.text.active = True

        self.search_button = menu.root.find_node("Search Button", True).get_content()
        self.search_button.register_pressed_callback(search_button_pressed_callback)
        
