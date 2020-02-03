import nanome
from nanome.util import Logs
from .similaritysearch_menu import SimilaritySearchMenu
class SimilaritySearch(nanome.PluginInstance):
    def start(self):
        self._menu = SimilaritySearchMenu(self)
        self._menu.build_menu()

    def on_run(self):
        self.menu.enabled = True
        self.update_menu(self.menu)

def main():
    plugin = nanome.Plugin('Similarity Search', 'A Nanome plugin to do similarity search using BLAST', 'other', False)
    plugin.set_plugin_class(SimilaritySearch)
    plugin.run('127.0.0.1', 8888)

if __name__ == '__main__':
    main()
