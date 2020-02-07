import nanome
from nanome.util import Logs
from .similaritysearch_menu import SimilaritySearchMenu
class SimilaritySearch(nanome.PluginInstance):
    def start(self):
        self._menu = SimilaritySearchMenu(self)
        self._menu.build_menu()
        nanome.util.Logs.debug("similarity search plugin started")

    def on_run(self):
        self.menu.enabled = True
        self.update_menu(self.menu)
        self._menu._request_refresh()
        nanome.util.Logs.debug("on run called")

    def on_complex_added(self):
        nanome.util.Logs.debug("Complex added: refreshing")
        self.request_refresh()

    def on_complex_removed(self):
        nanome.util.Logs.debug("Complex removed: refreshing")
        self.request_refresh()

    def request_refresh(self):
        self.request_complex_list(self.on_complex_list_received)
        nanome.util.Logs.debug("Complex list requested")
    
    def on_complex_list_received(self, complexes):
        Logs.debug("complex received: ", complexes)
        self._menu.change_complex_list(complexes)
    

def main():
    plugin = nanome.Plugin('Similarity Search', 'A Nanome plugin to do similarity search using BLAST', 'other', False)
    plugin.set_plugin_class(SimilaritySearch)
    plugin.run('127.0.0.1', 8888)

if __name__ == '__main__':
    main()
