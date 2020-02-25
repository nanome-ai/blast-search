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

    def update_result(self,results):
        Logs.debug("update result list called")
        self.result_list = []
        for result in results:
            clone = self.complex_item_prefab.clone()
            ln_btn = clone.get_children()[0]
            btn = ln_btn.get_content()
            btn.text.value.set_all(result.query)
            btn.complex = result
            self.result_list.append(clone)
        Logs.debug("result list is: ",self.result_list)
        self.output_list.items = self.result_list
        self.plugin.update_content(self.output_list)
        pass

    def build_menu(self):
        def search_button_pressed_callback(button):
            self.plugin.search_blast()
        
        def number_entered_callback(text):
            text_value = text._input_text
            if len(text._input_text) == 0:
                self.plugin.number_of_results = 10
            elif text_value.isnumeric():
                self.plugin.number_of_results = text_value
                Logs.debug(self.plugin.number_of_results)
            else:
                # error message
                pass

        menu = nanome.ui.Menu.io.from_json(os.path.join(os.path.dirname(__file__), 'SimilaritySearchMenu.json'))
        self.plugin.menu = menu

        self.show_list = menu.root.find_node("Input List", True).get_content()
        self.output_list = menu.root.find_node("Output List",True).get_content()
        self.number_input = menu.root.find_node("Number Input",True).get_content()
        self.number_input.register_changed_callback(number_entered_callback)

        # Create a prefab that will be used to populate the lists
        self.complex_item_prefab = nanome.ui.LayoutNode()
        self.complex_item_prefab.layout_orientation = nanome.ui.LayoutNode.LayoutTypes.horizontal
        child = self.complex_item_prefab.create_child_node()
        child.name = "complex_button"
        prefabButton = child.add_new_button()
        prefabButton.text.active = True

        self.search_button = menu.root.find_node("Search Button", True).get_content()
        self.search_button.register_pressed_callback(search_button_pressed_callback)
        
