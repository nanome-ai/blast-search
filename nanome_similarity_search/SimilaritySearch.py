import nanome
from nanome.util import Logs

class SimilaritySearch(nanome.PluginInstance):
    def start(self):
        menu = self.menu
        menu.title = 'Similarity Search'
        menu.width = 1
        menu.height = 1

        node = menu.root.create_child_node()
        node.add_new_label('hello, nanome!')

    def on_run(self):
        self.menu.enabled = True
        self.update_menu(self.menu)

def main():
    plugin = nanome.Plugin('Similarity Search', 'A Nanome plugin to do similarity search using BLAST', 'other', False)
    plugin.set_plugin_class(SimilaritySearch)
    plugin.run('127.0.0.1', 8888)

if __name__ == '__main__':
    main()
