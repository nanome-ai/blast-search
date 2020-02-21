import nanome
import os
from nanome.util import Logs
from .similaritysearch_menu import SimilaritySearchMenu
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML
 
class SimilaritySearch(nanome.PluginInstance):
    def start(self):
        self._menu = SimilaritySearchMenu(self)
        self._menu.build_menu()
        nanome.util.Logs.debug("similarity search plugin started")
        self.number_of_results = 3
        self.result_list = []

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

    def search_blast(self):
        Logs.debug("blast search test started")
        result_handle = NCBIWWW.qblast("blastn", "nt", "8332116")
        # with open(os.path.join(os.path.dirname(__file__),"my_blast.xml"), "w") as out_handle:
        #     out_handle.write(result_handle.read())
        # result_handle.close()
        # Logs.debug("blast XML file written")
        Logs.debug("qblast ended")
        for x in range(self.number_of_results):
            if x == 0:
                try:
                    blast_record = NCBIXML.read(result_handle)
                    self.result_list.append(blast_record)
                    Logs.debug("blast result #1: ",blast_record)
                except:
                    Logs.debug("No result found")
                    break
            else:
                try:
                    blast_record = next(blast_records)
                    self.result_list.append(blast_record)
                    Logs.debug("blast result #",x+1," ",blast_record)
                except:
                    Logs.debug("No more results")
                    break
                
        self.update_result()

    def update_result(self):
        self.menu.update_result(self.result_list)

def main():
    plugin = nanome.Plugin('Similarity Search', 'A Nanome plugin to do similarity search using BLAST', 'other', False)
    plugin.set_plugin_class(SimilaritySearch)
    plugin.run('127.0.0.1', 8888)

if __name__ == '__main__':
    main()
